#!/usr/bin/env python

from fastapi import FastAPI, status, Response, Request, Depends, Form, Query, HTTPException, Body
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from typing import Optional
from fastapi.middleware.cors import CORSMiddleware

import re
import threading
import socket

import sublist3r
import config as cfg

import schemas, models, auth
from db import SessionLocal, engine
from typing import List
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=cfg.setup_CORS['origin'],
    allow_credentials=cfg.setup_CORS['allow_credentials'],
    allow_methods=cfg.setup_CORS['allow_methods'],
    allow_headers=cfg.setup_CORS['allow_headers'],
)
app.mount("/public", StaticFiles(directory="build"), name="public")
templates = Jinja2Templates(directory="build")

# @app.middleware("http")
# async def check_login(res: Request, call_next):
#     response = await call_next(res)
#     return response

# @app.post("/api/sign-up", status_code=status.HTTP_201_CREATED)
# async def createUser(res: Response, username: str = Form(...),
#                      password: str = Form(...),
#                      email: str = Form(...),
#                      firstName: str = Form(...),
#                      lastName: str = Form(...)):

#     user = get_account_in_db(username)
#     if not user == None:
#         raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username is existed")

#     password = get_password_hash(password)

#     new_user = User(username, email, password, firstName, lastName)
#     new_user.save()

#     token = new_user.generate_token()

#     return {"status": True, "token":token}

# @app.post("/api/sign-in", status_code=status.HTTP_200_OK)
# async def login(res: Response, req: Request, form_data: OAuth2PasswordRequestForm = Depends()):
#     user = get_account_in_db(form_data.username)
#     if user == None:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Username or password wrong")
#     if not verify_password(form_data.password, user.password):
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Username or password wrong")
#     token = user.generate_token()
#     return {"status": True, "token": token}

#====================================================================================================


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/api/users", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    users = auth.get_users(db, skip, limit)
    return users


@app.get("/api/users/me", response_model=schemas.User)
def read_user(token:str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user = auth.get_current_user(db, token=token)
    return user


@app.post("/api/create-user", status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = auth.get_user_by_mail(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Email already registered")
    db_username = auth.get_user_by_username(db, username=user.username)
    if db_username:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Username already registered")
    auth.create_user(db, user=user)
    return {"detail": "Sign Up successful"}


@app.post("/api/token")
def login(res: Response, user: schemas.UserLogin, db: Session = Depends(get_db)):
    user = auth.authenticate_user(db, user.username, user.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password",
                            headers={"WWW-Authenticate": "Bearer"})
    token = auth.generate_token(data = {"user_id": user.id, "username": user.username})
    res.set_cookie(key="token", value=token['access_token'])
    res.headers['Authorization'] = "Bearer " + token['access_token']
    res.status_code = status.HTTP_200_OK
    return {"detail": "Login success", "access_token": token['access_token']}

#+====================================================================================================


@app.get("/api/{domain}", status_code=status.HTTP_200_OK)
async def check(res: Response,
                domain: str,
                ports: Optional[str] = None,
                bruteforce: Optional[bool] = False,
                engines: Optional[str] = None, token: str = Depends(oauth2_scheme)):
    if checkDomain(domain) == False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please input invalid domain")

    if engines != None:
        if checkEngine(engines.split(',')) == False:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")

    try:
        subdomains = await scan(domain, ports, bruteforce, engines)
    except:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Something error")

    if ports:
        ports = ports.split(',')
        try:
            pscan = portscan(subdomains, ports)
            subListPort = await pscan.run()
        except:
            raise HTTPException(status_code=status.HTTP_408_REQUEST_TIMEOUT, detail="Request timeout")

        if len(subListPort) > 0:
            # writeFileExcel(subListPort)
            return {"result": subListPort}
        else:
            return {"result": []}

    if len(subdomains) == 0:
        return {"result": []}
    else:
        new_subdomains = list(
            map(lambda subdomain: {
                "host": subdomain,
                'port': None
            }, subdomains))
        # writeFileExcel(new_subdomains)
        return {"result": new_subdomains}


async def scan(domain, port, bruteforce, engines):
    subdomains = sublist3r.main(domain,
                                40,
                                None,
                                ports=None,
                                silent=False,
                                verbose=False,
                                enable_bruteforce=bruteforce,
                                engines=engines)
    return subdomains


def checkDomain(domain):
    domain_check = re.compile(
        "^(http|https)?[a-zA-Z0-9]+([\-\.]{1}[a-zA-Z0-9]+)*\.[a-zA-Z]{2,}$")
    if not domain_check.match(domain):
        return False


def checkEngine(engines):
    print(engines)
    listEngine = [
        'baidu', 'yahoo', 'google', 'bing', 'ask', 'netcraft', 'dnsdumpster',
        'virustotal', 'threatcrowd', 'ssl', 'passivedns'
    ]
    for n in engines:
        if n not in listEngine:
            return False


class portscan():
    def __init__(self, subdomains, ports):
        self.subdomains = subdomains
        self.ports = ports
        self.lock = None

    def port_scan(self, host, ports, sublistPort):
        self.lock.acquire()
        for port in ports:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(2)
                result = s.connect_ex((host, int(port)))
                if result == 0:
                    print({"Host": host, "Port": port})
                    sublistPort.append({"host": host, "port": port})
                s.close()
            except Exception:
                pass
        self.lock.release()

    async def run(self):
        sublistPort = []
        threads = list()

        self.lock = threading.BoundedSemaphore(value=20)
        for subdomain in self.subdomains:
            t = threading.Thread(target=self.port_scan,
                                 args=(subdomain, self.ports, sublistPort))
            threads.append(t)
            t.start()

        for thread in threads:
            thread.join(2)

        # time.sleep(180)
        return sublistPort
