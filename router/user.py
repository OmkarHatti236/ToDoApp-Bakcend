from fastapi import APIRouter,Depends,HTTPException
from database import sessionLocal
from passlib.context import CryptContext
from starlette import status    
from .auth import get_current_user
from typing import Annotated
from sqlalchemy.orm import Session
from validation import *
from model import *


router=APIRouter(
    tags=['user']
)

bcrypt_context= CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_db():
    db=sessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency=Annotated[Session,Depends(get_db)]
user_dependency=Annotated[dict,Depends(get_current_user)]

@router.post('/update')
async def update_user(user:user_dependency,db:db_dependency,request:userVerification):
    user=db.query(Users).filter(Users.username==user.get('username')).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='wrong username or password')
    if not bcrypt_context.verify(request.password,user.hashed_password):
         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='wrong username or password')
    user.hashed_password=bcrypt_context.hash(request.new_password)
    db.commit()

    return {
        "status": "success",
        "message": "Password updated successfully"
    }

@router.post('/update/phone_num')
async def update_user(user:user_dependency,db:db_dependency,number:str):
    user=db.query(Users).filter(Users.username==user.get('username')).first()
    user.phone_number=number
    db.commit()

    return {
        "status": "success",
        "message": "phone unmber"
    }