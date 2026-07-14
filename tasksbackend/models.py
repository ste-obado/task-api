from database import Base
from sqlalchemy import ForeignKey, Integer,String,DateTime,Column,Boolean,DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

class User(Base):
    __tablename__="user"
    id=Column(Integer,primary_key=True,index=True)
    username=Column(String(100))
    email=Column(String(100),unique=True)
    is_active=Column(Boolean,default=True)
    password=Column(String(100))
    #python convinience replace join query in db
    tasks=relationship("Task",back_populates="user")#virtual db column
    

class Task(Base):
    __tablename__="tasks"
    user_id=Column(Integer,ForeignKey("user.id"))#actual db column
    id =Column(Integer,primary_key=True,index=True)
    title=Column(String(100))
    #python convinience replace join query in db
    user=relationship("User",back_populates="tasks")
    status=Column(String(50),default="pending")
    due_date=Column(DateTime,default=lambda: datetime.now(timezone.utc))


