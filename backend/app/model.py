

from sqlalchemy import Column, Integer, String, TIMESTAMP

from database import Base


class Post(Base):
    __tablename__ = 'posts'

    post_id=Column(Integer, primary_key=True,nullable=False,unique=True)
    author_name=Column(String(10,collation="utf8mb4_general_ci"), nullable=False)
    content=Column(String(255), nullable=False)
    created_at=Column(TIMESTAMP,nullable=False)
    type=Column(Integer, nullable=False,index=True)
    password=Column(String(255), nullable=False)