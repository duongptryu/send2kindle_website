
#===========================================================================================
from db.db import Base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from .associate_table import User_Domain
from passlib.hash import bcrypt



class User(Base):
    __tablename__ = "users"

    id=Column(Integer, primary_key=True, index=True)
    username=Column(String, unique=True)
    password_hashed=Column(String)
    email=Column(String)
    first_name=Column(String)
    last_name=Column(String)
    vip_member=Column(Boolean, default=False)
    domains = relationship("Domain", secondary=User_Domain, back_populates="users")

    def verify_password(self, password):
        return bcrypt.verify(password, self.password_hashed)

    def update_vip_member(self):
        self.vip_member = True

#===============================================================================================
