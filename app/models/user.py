
#===========================================================================================
from db.db import Base
from sqlalchemy import Column, Integer, String
from passlib.hash import bcrypt

class User(Base):
    __tablename__ = "users"

    id=Column(Integer, primary_key=True, index=True)
    username=Column(String, unique=True)
    password_hashed=Column(String)
    email=Column(String)
    first_name=Column(String)
    last_name=Column(String)

    def verify_password(self, password):
        return bcrypt.verify(password, self.password_hashed)

#===============================================================================================
