# from pymodm.connection import connect
# from pymodm.errors import ConnectionError
# from fastapi import HTTPException, status

# try:
#     connect("mongodb://localhost:27017/testDB", alias="my-app")
# except ConnectionError as identifier:
#     raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Can connect database")
#=============================================================================
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://postgres:201085@localhost:5432/testdb"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

#============================================================================
