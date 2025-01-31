from typing import List

from pydantic import BaseModel


class PostInfo(BaseModel):
    post_id: int
    author_name:str
    type:int

    class Config:
        orm_mode = True

class PostInfoList(BaseModel):
    total:int
    posts:List[PostInfo]

class PostDetail(BaseModel):
    post_id: int
    author_name: str
    content: str
    type: int

class CreatePost(BaseModel):
    content:str
    author_name:str
    type:int
    password:str


class DeleteRequest(BaseModel):
    password:str




