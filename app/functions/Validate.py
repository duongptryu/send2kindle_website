import re

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
