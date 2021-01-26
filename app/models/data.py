from db.db import Base
from sqlalchemy import Column, String, DateTime, Integer, Float
from sqlalchemy.orm import relationship
import time
from .associate_table import Domain_Port, User_Domain

class Data(Base):
    __tablename__ = "data"

    id = Column(Integer, primary_key=True, index=True)
    domain = Column(String)
    subdomain = Column(String)
    time = Column(Float, default=time.time())

    ports = relationship("Port", secondary=Domain_Port, back_populates = "domains")
    users = relationship("User", secondary=User_Domain, back_populates = "domains")
    # ports = relationship("Domain_Port", back_populates="")