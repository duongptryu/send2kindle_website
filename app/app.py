#!/usr/bin/env python

from fastapi import FastAPI, status, Response
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware

import re
import pandas as pd
import sublist3r

import config as cfg
import portScan as ps


app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=cfg.setup_CORS['origin'],
    allow_credentials=cfg.setup_CORS['allow_credentials'],
    allow_methods=cfg.setup_CORS['allow_methods'],
    allow_headers=cfg.setup_CORS['allow_headers'],
)



@app.get("/{domain}", status_code=status.HTTP_200_OK)
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
        pscan = ps.portscan(subdomains, ports)
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

# def writeFileExcel(sublist):
#     sublist_df = pd.DataFrame(sublist)
#     writer = pd.ExcelWriter('mult_sheets_1.xlsx')
#     sublsit_df.to_excel(writer, sheet_name='df_1', index=False)
#     sublsit_df.to_excel(writer, sheet_name='df_2', index=False)
#     sublsit_df.to_excel(writer, sheet_name='df_3', index=False)