#!/usr/bin/env python

from fastapi import FastAPI, status, Response, Request, Depends, Form, Query, HTTPException, Body, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from typing import Optional, List
from fastapi.middleware.cors import CORSMiddleware

import re
import time
import sublist3r
import core.config as cfg
from functions.ScanPort import portscan

from schemas.token import Token as SchemaToken
from schemas.user import User as SchemaUser, UserCreate as SchemaUserCreate, UserLogin as SchemaUserLogin

import models.user as ModelUser
import models.domain as ModelDomain
import models.subdomain as ModelSubdomain
import models.port as ModelPort
import models.associate_table as ModelAssociate

import auth.auth as auth
from db.db import SessionLocal, engine
from functions.Validate import checkEngine, checkDomain
from functions.domain_subdomain import add_sub_to_database, get_domain_like, get_id_domain, get_subdomains_and_filter, check_port_in_db, get_subdomains_port, add_port_to_exist_db_sub, add_sub_port_to_db, get_subdomains, scan_subdomains_port, filter_subdomain_port

from sqlalchemy.orm import Session

ModelUser.Base.metadata.create_all(bind=engine)
ModelDomain.Base.metadata.create_all(bind=engine)
ModelSubdomain.Base.metadata.create_all(bind=engine)
ModelAssociate.Base.metadata.create_all(bind=engine)
ModelPort.Base.metadata.create_all(bind=engine)

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

#====================================================================================================


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/api/users",
         response_model=List[SchemaUser],
         status_code=status.HTTP_200_OK)
def read_users(skip: int = 0,
               limit: int = 100,
               db: Session = Depends(get_db),
               token: str = Depends(oauth2_scheme)):
    users = auth.get_users(db, skip, limit)
    return users


@app.get("/api/users/me")
def read_user(token: str = Depends(oauth2_scheme),
              db: Session = Depends(get_db)):
    user = auth.get_current_user(db, token=token)
    return {
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "vip_member": user.vip_member
    }


@app.post("/api/create-user", status_code=status.HTTP_201_CREATED)
def create_user(user: SchemaUserCreate, db: Session = Depends(get_db)):
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


@app.post("/api/token", status_code=status.HTTP_200_OK)
def login(res: Response,
          user: OAuth2PasswordRequestForm = Depends(),
          db: Session = Depends(get_db)):

    user = auth.authenticate_user(db, user.username, user.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password",
                            headers={"WWW-Authenticate": "Bearer"})
    token = auth.generate_token(data={
        "user_id": user.id,
        "username": user.username
    })
    res.set_cookie(key="token", value=token['access_token'])
    res.headers['Authorization'] = "Bearer " + token['access_token']
    return {"detail": "Login success", "access_token": token['access_token']}


@app.get("/api/update-vip-member")
def update_user(token: str = Depends(oauth2_scheme),
                db: Session = Depends(get_db)):
    user = auth.get_current_user(db, token)
    if user == None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Please login")
    if user.vip_member:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Already a vip member")
    user.update_vip_member()
    db.add(user)
    db.commit()
    return user


#+====================================================================================================


@app.get("/api/{domain}", status_code=status.HTTP_200_OK)
async def check(background_tasks: BackgroundTasks,
                res: Response,
                domain: str,
                ports: Optional[str] = None,
                bruteforce: Optional[bool] = False,
                engines: Optional[str] = None,
                token: str = Depends(oauth2_scheme),
                db: Session = Depends(get_db)):
    if checkDomain(domain) == False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Please input invalid domain")

    if engines != None:
        if checkEngine(engines.split(',')) == False:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Bad request")

    user = auth.get_current_user(db, token)
    if user == None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Please login")
    flag = user.vip_member
    result = []
    if flag:
        # try:
        domain_exist = get_domain_like(db, domain)
        if domain_exist:
            if timeprocess(domain_exist) < 72800:
                if ports:
                    if check_port_in_db(db, ports, domain_exist):
                        subdomains = get_subdomains_port(
                            db, domain_exist.id, ports)
                        result = filter_subdomain_port(subdomains, ports)
                    else:
                        background_tasks.add_task(scan_port_in_background, db,
                                                  domain_exist, ports,
                                                  background_tasks)
                        res.status_code = status.HTTP_202_ACCEPTED
                        return {
                            "detail":
                            "Receiving request, we are processing , please comeback later"
                        }
                else:
                    subdomains = get_subdomains(db, domain_exist.id)
                    result = filter_subdomain_port(subdomains, None)
                return {"result": result}
            else:
                background_tasks.add_task(scan_for_new_session, db,
                                          domain_exist, domain, ports,
                                          bruteforce, engines,
                                          background_tasks)
                res.status_code = status.HTTP_202_ACCEPTED
                return {
                    "detail":
                    "Receiving request, we are processing , please comeback later"
                }
                # result = filter_subdomain_port(subdomains, ports)
                # return {"result": result}
        else:
            background_tasks.add_task(scan_in_background, db, ports, domain,
                                      bruteforce, engines, background_tasks)
            res.status_code = status.HTTP_202_ACCEPTED
            return {
                "detail":
                "Receiving request, we are processing , please comeback later"
            }
        # except:
        # raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        #                     detail="Something error")
    else:
        if ports:
            raise HTTPException(
                status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                detail="Just vip member allowed to use this feature")

        domain_exist_in_user = check_domain_in_user_db(user, domain)
        domain_exist = get_domain_like(db, domain)
        if domain_exist_in_user:
            if timeprocess(domain_exist) < 72800:
                subdomains = get_subdomains(db, domain_exist.id)
                result = filter_subdomain_port(subdomains, None)
                return {"result": result}
            else:
                background_tasks.add_task(scan_for_new_session, db,
                                          domain_exist, domain, ports,
                                          bruteforce, engines,
                                          background_tasks)
                res.status_code = status.HTTP_202_ACCEPTED
                return {
                    "detail":
                    "Receiving request, we are processing , please comeback later"
                }
        else:
            if domain_exist:
                background_tasks.add_task(scan_for_new_session, db,
                                          domain_exist, domain, ports,
                                          bruteforce, engines,
                                          background_tasks)
                background_tasks.add_task(add_domain_to_normal_account, db,
                                          user, domain)
                res.status_code = status.HTTP_202_ACCEPTED
                return {
                    "detail":
                    "Receiving request, we are processing , please comeback later"
                }
            else:
                background_tasks.add_task(scan_in_background, db, ports,
                                          domain, bruteforce, engines,
                                          background_tasks)
                background_tasks.add_task(add_domain_to_normal_account, db,
                                          user, domain)
                res.status_code = status.HTTP_202_ACCEPTED
                return {
                    "detail":
                    "Receiving request, we are processing , please comeback later"
                }


async def add_domain_to_normal_account(db: Session, user: ModelUser,
                                       domain: str):
    # import pdb; pdb.set_trace()
    domain_exist = db.query(ModelDomain.Domain).filter(
        ModelDomain.Domain.domain == domain).first()
    user.domains.append(domain_exist)
    db.add(user)
    db.commit()


def check_domain_in_user_db(user: ModelUser, domain_arg: str):
    # import pdb; pdb.set_trace()
    for domain in user.domains:
        if domain_arg == domain.domain:
            return domain
    return None


async def scan_for_new_session(db: Session, domain_exist, domain, ports,
                               bruteforce, engines,
                               background_tasks: BackgroundTasks):
    db.delete(domain_exist)
    db.commit()
    if ports:
        subdomains = await scan_subdomains_port(subdomains, ports)
        add_sub_port_to_db(db, subdomains, ports, domain)
    else:
        subdomains = await scan(domain, ports, bruteforce, engines)
        add_sub_to_database(db, domain, subdomains)


async def scan_port_in_background(db: Session, domain_exist, ports,
                                  background_tasks: BackgroundTasks):
    subdomains = get_subdomains(db, domain_exist.id)
    new_sub = await scan_subdomains_port(subdomains, ports)
    add_port_to_exist_db_sub(db, domain_exist.id, ports, new_sub)


async def scan_in_background(db: Session, ports, domain, bruteforce, engines,
                             background_tasks: BackgroundTasks):
    subdomains = await scan(domain, ports, bruteforce, engines)
    add_sub_to_database(db, domain, subdomains)
    if (len(subdomains) != 0):
        if ports:
            subdomain_port = await scan_subdomains_port(subdomains, ports)
            add_sub_port_to_db(db, subdomain_port, ports, domain)


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


def timeprocess(domain_obj):
    time_old = domain_obj.time
    time_new = time.time()
    return time_new - time_old
