# from sqlalchemy import Column,Integer,String,ForeignKey,Boolean
# from sqlalchemy.orm import declarative_base



# Base=declarative_base()

# class Users(Base):
#     __tablename__='Users'
#     id=Column(Integer,primary_key=True)
#     email=Column(String,unique=True)
#     username=Column(String,unique=True)
#     first_name=Column(String)
#     last_name=Column(String)
#     hashed_password=Column(String)
#     is_active=Column(Boolean,default=True)
#     role=Column(String)

# class Todos(Base):
#     __tablename__='Todos'
#     id=Column(Integer,primary_key=True)
#     title=Column(String)
#     description=Column(String)
#     priority=Column(Integer)
#     complete=Column(String,default=False)
#     user_id=Column(Integer,ForeignKey('Users.id'))
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Users(Base):
    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True)
    username = Column(String(100), unique=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    hashed_password = Column(String(255))
    is_active = Column(Boolean, default=True)
    role = Column(String(50))
    phone_number=Column(String(15))


class Todos(Base):
    __tablename__ = 'Todos'

    id = Column(Integer, primary_key=True)
    title = Column(String(200))
    description = Column(String(500))
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey('Users.id'))
