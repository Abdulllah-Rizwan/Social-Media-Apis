from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint;


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class Create_Post(PostBase):
    pass

class User_Out(BaseModel):
    id: int
    name: str
    email: str
    created_at: datetime

class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: User_Out
    
    class Config:
        orm_mode = True
        exclude = ['updated_at']

class Post_Out(BaseModel):
    Post: Post
    Votes: int

    class Config:
        orm_mode = True

class User_Create(BaseModel):
    name: str
    email: EmailStr
    password: str


class Login_User(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    token: str
    token_type: str

class Token_data(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir: conint(ge=0, le=1)