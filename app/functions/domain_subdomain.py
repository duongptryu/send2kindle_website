from sqlalchemy.orm import Session
import models.domain as ModelDomain
import models.subdomain as ModelSubdomain
import models.port as ModelPort
from typing import List
from .ScanPort import portscan

def add_sub_to_database(db: Session, domain: str, subdomain: List[str]):
    db_domain = ModelDomain.Domain(domain=domain)
    db.add(db_domain)
    db.commit()
    domain_id = get_id_domain(db, domain)
    db_sub = db.bulk_save_objects([
        ModelSubdomain.Subdomain(domain_id=domain_id, subdomain=sub)
        for sub in subdomain
    ])
    db.commit()


def get_id_domain(db: Session, domain: str):
    db_domain = db.query(ModelDomain.Domain).filter(
        ModelDomain.Domain.domain == domain).first()
    return db_domain.id


def get_domain_like(db: Session, domain: str):
    return db.query(ModelDomain.Domain).filter(
        ModelDomain.Domain.domain.like("%" + domain + "%")).first()

def get_subdomains_and_filter(db: Session, id_domain_exist):
    subdomains = db.query(ModelSubdomain.Subdomain).filter(
            ModelSubdomain.Subdomain.domain_id == id_domain_exist).all()

    new_sub = list(
            map(lambda row: 
                row.subdomain
            , subdomains))
    return new_sub


def check_port_in_db(db: Session, port_arg, domain_obj):
    for port in domain_obj.ports:
        if port.port == int(port_arg):
            return True
    return False

def get_subdomains_port(db: Session, domain_id, port_arg):
    subdomains = db.query(ModelSubdomain.Subdomain).filter(ModelSubdomain.Subdomain.domain_id == domain_id).all()
    new_sub = []
    for sub in subdomains:
        for x in sub.ports:
            if x.port == int(port_arg):
                new_sub.append(sub.subdomain)
    return new_sub

def add_port_to_exist_db_sub(db: Session, domain_id, port, sub_port):
    domain = db.query(ModelDomain.Domain).filter(
        ModelDomain.Domain.id == domain_id).first()
    subdomains = domain.subdomains
    port_obj = db.query(ModelPort.Port).filter(ModelPort.Port.port == port).first()
    if port_obj == None:
        port_obj = ModelPort.Port(port=port)
    domain.ports.append(port_obj)
    db.add(domain)
    db.commit()
    # import pdb; pdb.set_trace()
    for sub in subdomains:
        if sub.subdomain in sub_port:
            sub.ports.append(port_obj)
            db.add(sub)
    db.commit()

def add_sub_port_to_db(db: Session, subdomains, port, domain):
    domain_obj = db.query(ModelDomain.Domain).filter(ModelDomain.Domain.domain == domain).first()
    if domain_obj == None:
        domain_obj = ModelDomain.Domain(domain=domain)
        db.add(domain_obj)
        db.commit()
    port_obj = ModelPort.Port(port=port)
    domain_obj.ports.append(port_obj)
    db.add(domain_obj)
    db.commit()
    domain_id = domain_obj.id
    # import pdb; pdb.set_trace()
    for subdomain in domain_obj.subdomains:
        if subdomain.subdomain in subdomains:
            subdomain.ports.append(port_obj)
    db.commit()


def get_subdomains(db, domain_exist_id):
    domain = db.query(ModelDomain.Domain).filter(
        ModelDomain.Domain.id == domain_exist_id).first()
    subdomains = domain.subdomains
    new_sub = list(map(lambda row: row.subdomain, subdomains))
    return new_sub


async def scan_subdomains_port(subdomains, ports):
    ports = ports.split(',')
    try:
        pscan = portscan(subdomains, ports)
        new_sub = await pscan.run()
    except:
        raise HTTPException(status_code=status.HTTP_408_REQUEST_TIMEOUT,
                            detail="Request timeout")
    return new_sub


def filter_subdomain_port(subdomains, ports):
    if ports:
        sub_list = list(
            map(lambda subdomain: {
                "host": subdomain,
                'port': ports
            }, subdomains))
    else:
        sub_list = list(
            map(lambda subdomain: {
                "host": subdomain,
                'port': None
            }, subdomains))
    return sub_list