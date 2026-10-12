from pydantic import BaseModel,Field


class userRequest(BaseModel):
    email:str
    username:str
    first_name:str
    last_name:str
    password:str=Field(min_length=5)
    active:bool
    role:str
    phone_number:str

class Token(BaseModel):
    access_token:str
    type:str

class todoRequest(BaseModel):
    title:str
    description:str
    priority:int
    complete:bool

class userVerification(BaseModel):
    password:str
    new_password:str=Field(min_length=5)

