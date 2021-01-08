#!/usr/bin/env python

from fastapi import FastAPI, status, Response, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from typing import Optional
from fastapi.middleware.cors import CORSMiddleware

import re
import threading
import socket
# import pandas as pd
import sublist3r

import config as cfg


app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=cfg.setup_CORS['origin'],
    allow_credentials=cfg.setup_CORS['allow_credentials'],
    allow_methods=cfg.setup_CORS['allow_methods'],
    allow_headers=cfg.setup_CORS['allow_headers'],
)

app.mount("/static", StaticFiles(directory="../build/static"), name="static")

templates = Jinja2Templates(directory="../build")

# @app.get("/test")
# def test():
#     pass

@app.get("/", response_class=HTMLResponse)
async def serve_spa(request: Request, ):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api/{domain}", status_code=status.HTTP_200_OK)
async def check(res: Response, domain: str, ports: Optional[str]=None, bruteforce: Optional[bool]=False, engines: Optional[str]=None ):

    if checkDomain(domain) == False:
        res.status_code = status.HTTP_400_BAD_REQUEST
        return {"Error": "Please input valid domain"}

    if engines != None:
        if checkEngine(engines.split(',')) == False:
            res.status_code = status.HTTP_400_BAD_REQUEST
            return {"Error": "Bad Input"}

    try:
        subdomains = scan(domain, ports, bruteforce, engines)
    except expression as identifier:
        res.status_code = status.HTTP_504_GATEWAY_TIMEOUT   
        return {"Error": "Something error"}

    if ports:
        ports = ports.split(',')
        pscan = portscan(subdomains, ports)
        subListPort = pscan.run()   
        if len(subListPort) > 0:
            # writeFileExcel(subListPort)
            return {"result": subListPort}
        else:
            return {"result": []}

    if len(subdomains) == 0:
        return {"result": []}
    else:
        new_subdomains = list(map(lambda subdomain: {"host": subdomain, 'port': None}, subdomains))
        # writeFileExcel(new_subdomains)
        return {"result": new_subdomains}



def scan(domain, port, bruteforce, engines):
    subdomains = sublist3r.main(domain, 40, None, ports=None, silent=False, verbose= False, enable_bruteforce= bruteforce, engines=engines)
    return subdomains



def checkDomain(domain):
    domain_check = re.compile("^(http|https)?[a-zA-Z0-9]+([\-\.]{1}[a-zA-Z0-9]+)*\.[a-zA-Z]{2,}$")
    if not domain_check.match(domain):
        return False


def checkEngine(engines):
    print(engines)
    listEngine = ['baidu', 'yahoo', 'google', 'bing', 'ask', 'netcraft', 'dnsdumpster', 'virustotal', 'threatcrowd', 'ssl', 'passivedns']
    for n in engines:
            if n not in listEngine:
                return False



class portscan():
    def __init__(self, subdomains, ports):
        self.subdomains = subdomains
        self.ports = ports
        self.lock = None
        self.subList = []

    def port_scan(self, host, ports):
        openports = []
        self.lock.acquire()
        for port in ports:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(2)
                result = s.connect_ex((host, int(port)))
                if result == 0:
                    openports.append(port)
                s.close()
            except Exception:
                pass
        self.lock.release()
        if len(openports) > 0:
            self.subList.append({"host": host, "port": port})

    def run(self):
        self.lock = threading.BoundedSemaphore(value=20)
        for subdomain in self.subdomains:
            t = threading.Thread(target=self.port_scan, args=(subdomain, self.ports))
            t.start()
        return self.subList