from pydantic import BaseModel
from typing import List


class BaseBlog(BaseModel):
    title: str
    body: str


class Blog(BaseBlog):
    class Config:
        orm_mode = True


class BaseUser(BaseModel):
    name: str
    email: str

    class Config:
        orm_mode = True


class User(BaseUser):
    password: str


class ShowUser(BaseModel):
    name: str
    email: str
    blogs: List[Blog] = []

    class Config:
        orm_mode = True


class ShowBlog(BaseModel):
    title: str
    body: str
    creator: BaseUser

    class Config:
        orm_mode = True
