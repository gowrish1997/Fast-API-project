import jwt
from datetime import timedelta,datetime
from pwdlib import PasswordHash
from app.config.app_config import getAppConfig

def hashPassword(password:str)->str:
    hasher = PasswordHash.recommended()
    return hasher.hash(password)

def verifyPassword(password:str,hashed_password:str)->bool:
    hasher = PasswordHash.recommended()
    return hasher.verify(password,hashed_password) 

def createToken(data:dict)->str:
    cofig=getAppConfig()
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=cofig.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, cofig.secret_key, algorithm=cofig.algorithm or "HS256")
    return encoded_jwt

def decodeAccessToken(token:str)->dict:
    cofig=getAppConfig()
    return jwt.decode(token, cofig.secret_key, algorithms=[cofig.algorithm or "HS256"])