from fastapi import APIRouter,Depends,HTTPException
from database import sessionLocal
from starlette import status    
from .auth import get_current_user
from typing import Annotated
from sqlalchemy.orm import Session
from validation import *
from model import *


router=APIRouter(
    tags=['Admin']
)

def get_db():
    db=sessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency=Annotated[Session,Depends(get_db)]
user_dependency=Annotated[dict,Depends(get_current_user)]


@router.get('/',status_code=status.HTTP_200_OK)
async def get_all(user:user_dependency,db:db_dependency):
    if not user.get('user_role')=='admin':
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='only admin can access this')
    return db.query(Todos).all()