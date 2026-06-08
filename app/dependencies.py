from jwt.exceptions import JWTError
from fastapi import status
from fastapi import HTTPException
from fastapi.security.oauth2 import OAuth2PasswordBearer
from typing import Annotated
from fastapi import Depends
from app.helper import decodeAccessToken

oauth2_schema=OAuth2PasswordBearer(tokenUrl="auth/login")

def authenticte_user(token:Annotated[str,Depends(oauth2_schema)]):
    try:
        user=decodeAccessToken(token)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token")
    return user