from db.db import Base
from sqlalchemy import Column, String, DateTime, Integer, Float
from sqlalchemy.orm import relationship
import time
from .associate_table import Domain_Port

class Domain(Base):
    __tablename__ = "domains"

    id = Column(Integer, primary_key=True, index=True)
    domain = Column(String, unique=True)
    time = Column(Float, default=time.time())

    subdomains = relationship("Subdomain", back_populates = "domain", cascade="all, delete")
    ports = relationship("Port", secondary=Domain_Port, back_populates = "domains")