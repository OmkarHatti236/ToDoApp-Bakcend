from fastapi import APIRouter,Depends,HTTPException
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from jose import jwt,JWTError
from database import sessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status
from validation import userRequest,Token
from model import *
from passlib.context import CryptContext
from datetime import datetime,timedelta,timezone




router=APIRouter(
    prefix='/auth',
    tags=['Auth']
)
SECRET_KEY='4832bb06a9d951b9dfc67adacb5006aa2dc49a692767950b1c17d7ae5a14bec2'
ALGORITHM='HS256'

bcrypt_context= CryptContext(schemes=["bcrypt"], deprecated="auto")
Oauth2_bearer=OAuth2PasswordBearer(tokenUrl='/auth/token')

def get_db():
    db=sessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency=Annotated[Session,Depends(get_db)]


def authenticate_user(username:str,password:str,db):
     user=db.query(Users).filter(Users.username==username).first()
     if user is None:
          return False
     if not bcrypt_context.verify(password,user.hashed_password):
          return False
     return user

def create_access_token(username:str,id:int,role:str,expiry:timedelta):
     encode={'username':username,'id':id,'role':role}
     expire=datetime.now(timezone.utc)+expiry
     encode.update({'exp':expire})
     return jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)

async def get_current_user(token:Annotated[str,Depends(Oauth2_bearer)]):
     try:
          payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
          username=payload.get('username')
          id=payload.get('id')
          role=payload.get('role')
          return {'username':username,'user_id':id,'user_role':role}
     except JWTError:
          raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='failed while extracting JWT')


@router.get('')
async def all_users(db:db_dependency):
     return db.query(Users).all()
     



@router.post('/',status_code=status.HTTP_201_CREATED)
async def add_user(db:db_dependency,request:userRequest):
       new_user=Users(
            email=request.email,
            username=request.username,
            first_name=request.first_name,
            last_name=request.last_name,
            hashed_password=bcrypt_context.hash(request.password),
            is_active=request.active,
            role=request.role,
            phone_number=request.phone_number
       )
       db.add(new_user)
       db.commit()

       return {
        "message": "User created successfully",
        "user_id": new_user.id
    }

@router.post('/token',response_model=Token)
async def login_for_access_token(form_data:Annotated[OAuth2PasswordRequestForm,Depends()],db:db_dependency):
     user=authenticate_user(form_data.username,form_data.password,db)
     if not user:
          raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='could not authrize user')
     token=create_access_token(user.username,user.id,user.role,timedelta(minutes=20))
     return {
          'access_token':token,
          'type':'bearer'
     }