from db.db import Base
from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.orm import relationship
import datetime
from .associate_table import Domain_Port

class Domain(Base):
    __tablename__ = "domains"

    id = Column(Integer, primary_key=True, index=True)
    domain = Column(String, unique=True)
    time = Column(DateTime, default=datetime.datetime.utcnow())

    subdomains = relationship("Subdomain", back_populates = "domain")
    ports = relationship("Port", secondary=Domain_Port, back_populates = "domains")