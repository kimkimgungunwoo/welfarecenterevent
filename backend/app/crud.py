from typing import List

from model import Post
import schema
from sqlalchemy.orm import Session
from datetime import datetime

def create_post(post:schema.CreatePost,db:Session)->Post:
    db_post=Post(
        content=post.content,
        author_name=post.author_name,
        type=post.type,
        password=post.password,
        created_at=datetime.utcnow()
    )

    db.add(db_post)
    db.commit()
    db.refresh(db_post)

    return db_post

def find_post_by_id(id:int,db:Session):
    return db.query(Post).filter_by(post_id=id).first()
def post_to_postinfo(posts):
    rst = []
    for post in posts:
        rst.append(schema.PostInfo(post_id=post.post_id,
                                   author_name=post.author_name,
                                   type=post.type,
                                   ))
    return rst

def read_post(db: Session, limit: int, offset: int):
    total = db.query(Post).count()
    posts = post_to_postinfo(
        db.query(Post)
        .order_by(Post.post_id.desc())  # post_id 기준으로 내림차순 정렬
        .offset(offset)
        .limit(limit)
        .all()
    )
    return total, posts

def read_post_by_username(username: str, db: Session):
    return db.query(Post).filter_by(author_name=username).order_by(Post.post_id.desc()).all()

def search_post_by_username(username: str, limit: int, offset: int, db: Session):
    base_query = db.query(Post).filter(Post.author_name.like(f"%{username}%"))
    total = base_query.count()
    posts = post_to_postinfo(
        base_query
        .order_by(Post.post_id.desc())  # post_id 기준으로 내림차순 정렬
        .offset(offset)
        .limit(limit)
        .all()
    )
    return total, posts

def delete_post_by_password(Post,password:str,db:Session):
    if password==Post.password:
        db.delete(Post)
        db.commit()
        return True
    return False

