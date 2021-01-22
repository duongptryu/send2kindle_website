from db.db import Base
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .associate_table import Subdomain_Port

class Subdomain(Base):
    __tablename__ = "subdomains"

    id = Column(Integer, primary_key=True, index=True)
    subdomain = Column(String, unique=True)
    domain_id = Column(Integer, ForeignKey("domains.id"))

    domain = relationship("Domain", back_populates="subdomains")
    ports = relationship("Port", secondary=Subdomain_Port, back_populates="subdomains")
    

