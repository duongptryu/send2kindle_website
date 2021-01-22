from db.db import Base
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .associate_table import Domain_Port, Subdomain_Port

class Port(Base):
    __tablename__ = "ports"
    id = Column(Integer, primary_key=True)
    port = Column(Integer,unique=True)

    domains = relationship("Domain", secondary=Domain_Port, back_populates="ports")
    subdomains = relationship("Subdomain", secondary=Subdomain_Port, back_populates="ports")