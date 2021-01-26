
#======================================================================================================
from sqlalchemy.orm import Session

from schemas.token import Token as SchemaToken
from schemas.user import User as SchemaUser, UserCreate as SchemaUserCreate, UserLogin as SchemaUserLogin
from models.user import User

from passlib.hash import bcrypt
from jose import JWTError, jwt
from typing import Optional
from datetime import datetime, timedelta
from fastapi import HTTPException, status

SECRET_KEY = "f41dc46df8ccc52adfd825998d6a05d7c6b3a01e0b0fe561f32287c2b32eabaa"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def get_current_user(db: Session, token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    # import pdb; pdb.set_trace()
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise credentials_exception
    return user

def get_user_by_mail(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def create_user(db: Session, user: SchemaUserCreate):
    hashed_password = bcrypt.hash(user.password)
    db_user = User(username=user.username,
                          email=user.email,
                          password_hashed=hashed_password,
                          first_name=user.first_name,
                          last_name=user.last_name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    print(db_user)
    return db_user

def authenticate_user(db: Session, username: str, password: str):
    db_user = get_user_by_username(db=db, username=username)
    if not db_user:
        return False
    if not db_user.verify_password(password):
        return False
    return db_user

def generate_token(data: dict, expires_delta: Optional[timedelta] = None):
    encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    encode.update({"exp": expire})
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}
#========================================================================================================