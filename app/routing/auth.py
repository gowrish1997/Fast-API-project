from fastapi import status
from fastapi import HTTPException
from typing import Annotated

from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.models.user import Register,Login
from app.database.schema import User
from app.helper import hashPassword,verifyPassword,createToken


from sqlalchemy import select


router=APIRouter(tags=["Auth"],prefix="/auth")

@router.post("/login")
def login(user:Login,db:Annotated[Session, Depends(get_db)]):
    stmt=select(User).where(User.email == user.email)
    result = db.execute(stmt)
    existing_user = result.scalars().first()
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="User not found")
    if not verifyPassword(user.password, existing_user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid password")
    return {"user":existing_user,"token": createToken(existing_user.model_dump())}
    

@router.post("/register")
def register(user: Register, db: Annotated[Session, Depends(get_db)]):
    stmt = select(User).where(User.email == user.email)
    result = db.execute(stmt)
    if result.scalars().first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="User already exists")
    new_user = User(username=user.username, email=user.email, password=hashPassword(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user.model_dump()