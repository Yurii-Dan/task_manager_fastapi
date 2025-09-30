from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from .database import Base
from sqlalchemy.orm import relationship
from datetime import datetime

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    name = Column(String,unique=True,nullable=False,index=True)
    tasks = relationship("Task", back_populates="category")

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)    
    status = Column(String, default="new", index=True, nullable=False)  # "new", "in_progress", "done"
    deadline = Column(DateTime, nullable=True)
    
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    category = relationship("Category", back_populates="tasks")

