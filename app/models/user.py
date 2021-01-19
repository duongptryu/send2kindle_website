# from pymongo.write_concern import WriteConcern
# import db
# from pymodm import MongoModel, fields
# from pymodm.errors import ValidationError


# def is_email_address(string):
#         if not string.endswith("@gmail.com"):
#             raise ValidationError("Email address must be valid gmail account.")

# class User(MongoModel):
#     id = fields.ObjectId()
#     username = fields.CharField(required=True)
#     email = fields.EmailField(required=True)
#     password = fields.CharField(required=True, min_length=6)
#     first_name = fields.CharField(required=True, max_length=32)
#     last_name = fields.CharField(required=True, max_length=32)
#     tokens = fields.ListField()
#     role = fields.CharField()

#     class Meta:
#         write_concern = WriteConcern(j=True)
#         connection_alias = 'my-app'
    
#     def generate_token():
#         to_encode = {
#             "data": self.role
#         }
#         if expires_delta:
#             expires = datetime.utcnow() + expires_delta
#         else:
#             expire = datetime.utcnow() + timedelta(minutes=15)
#         to_encode['exp'] = expire
#         jwt_encode = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#         self.tokens.append(jwt_encode)
#         return jwt_encode


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

# from tortoise import fields
# from tortoise.models import Model
# from passlib.hash import bcrypt
# from tortoise.contrib.pydantic import pydantic_model_creator

# class User(Model):
#     id = fields.IntField(pk=True)
#     username = fields.CharField(50, unique=True)
#     password_hash = fields.CharField(128)
#     email = fields.CharField(unique=True, max_length=255)
#     first_name = fields.CharField(255)
#     last_name = fields.CharField(255)

#     def verify_password(self, password):
#         return bcrypt.verify(password, self.password_hash)

# User_Pydantic = pydantic_model_creator(User, name="User")
# UserIn_Pydantic = pydantic_model_creator(User, name="UserIn", exclude_readonly=True)