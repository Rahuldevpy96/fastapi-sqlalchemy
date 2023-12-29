from sqlalchemy import Boolean,Column,ForeignKey,Integer,String
from .database import Base
from sqlalchemy.orm import relationship


class BlogModel(Base):
    __tablename__="blog"
    id=Column(Integer,primary_key=True,index=True)
    title=Column(String)
    body=Column(String)
    users_id=Column(Integer, ForeignKey('users.id'))
    creator=relationship('UserModel',back_populates="blog")

class UserModel(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String)
    email=Column(String)
    password=Column(String)
    blog=relationship('BlogModel',back_populates="creator")

