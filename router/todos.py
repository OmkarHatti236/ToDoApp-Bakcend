from fastapi import APIRouter,Depends,HTTPException
from database import sessionLocal
from starlette import status    
from .auth import get_current_user
from typing import Annotated
from sqlalchemy.orm import Session
from validation import *
from model import *


router=APIRouter(
    prefix='/todo',
    tags=['Todos']
)

def get_db():
    db=sessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency=Annotated[Session,Depends(get_db)]
user_dependency=Annotated[dict,Depends(get_current_user)]

@router.get('/all',status_code=status.HTTP_200_OK)
async def  get_all(user:user_dependency,db:db_dependency):
    return db.query(Todos).filter(Todos.user_id==user.get('user_id')).all()

@router.get('/by_id/{id}',status_code=status.HTTP_200_OK)
async def  get_by_id(user:user_dependency,db:db_dependency,id:int):
    result=db.query(Todos)\
        .filter(Todos.id==id)\
        .filter(Todos.user_id==user.id)\
        .first()

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Todo Not Found')
    return result

@router.post('/add',status_code=status.HTTP_201_CREATED)
async def  add_todo(user:user_dependency,db:db_dependency,todo:todoRequest):
    new_todo=Todos(**todo.model_dump(),user_id=user.get('user_id'))
    db.add(new_todo)
    db.commit()

    return{
            "status": "created",
            "message": f"todo with id:{new_todo.id} created"
        }

@router.put('/update',status_code=status.HTTP_201_CREATED)
async def  add_todo(user:user_dependency,db:db_dependency,todo:todoRequest,id:int):
    result=db.query(Todos).filter(Todos.id==id).first()
    if result is None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    result.title=todo.title
    result.description=todo.description
    result.priority=todo.priority
    result.complete=todo.complete

    db.commit()

    return {'status':'success',
            'message':f'todo with id:{result.id} updated'
            }

@router.delete('/delete', status_code=status.HTTP_200_OK)
async def  add_todo(user:user_dependency,db:db_dependency,id:int):
    result=db.query(Todos)\
        .filter(Todos.id==id)\
        .filter(Todos.user_id==user.get('user_id'))\
        .first()
    if result is None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="TODO not found")
    
    db.delete(result)
    db.commit()

    return {'status':'success',
            'message':f'todo with id:{result.id} deletd'
            }