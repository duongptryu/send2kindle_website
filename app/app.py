from fastapi import FastAPI, status, Response
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
import re


import sublist3r


app=FastAPI()


origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)

# @app.get("/", status_code=status.HTTP_404_NOT_FOUND)
# def notFound():
#     return {"Error": "Not Found"}

@app.get("/{domain}", status_code=status.HTTP_200_OK)
async def check(res: Response, domain: str, port: Optional[str]=None, bruteforce: Optional[bool]=False, engines: Optional[str]=None ):

    
    if checkDomain(domain) == False:
        res.status_code = status.HTTP_400_BAD_REQUEST
        return {"Error": "Please input valid domain"}

    if engines != None:
        if checkEngine(engines.split(',')) == False:
            res.status_code = status.HTTP_400_BAD_REQUEST
            return {"Error": "Bad Input"}

    try:
        subdomain = await scan(domain, port, bruteforce, engines)
    except expression as identifier:
        res.status_code = status.HTTP_504_GATEWAY_TIMEOUT   
        return {"Error": "Something error"}
    # if port:
    #     portScan(subdomain, port)
    return {"result": "No result", "port":port} if len(subdomain) == 0 else {"result": subdomain, "port": port}



async def scan(domain, port, bruteforce, engines):
    subdomains = sublist3r.main(domain, 40, None, ports=port, silent=False, verbose= False, enable_bruteforce= bruteforce, engines=engines)
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

# def portScan(port, subdomains):
#     openports = []
#     for port in ports:
#             try:
#                 s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#                 s.settimeout(2)
#                 result = s.connect_ex((host, int(port)))
#                 if result == 0:
#                     openports.append(port)
#                 s.close()
#             except Exception:
#                 pass
    
#     print(openports)

