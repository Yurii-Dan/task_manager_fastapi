from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional, List, Literal
from datetime import date, datetime
from pydantic import Field

class CategoryBase(BaseModel):
    name: str


class CategoryCreate(CategoryBase):
    pass


class Category(CategoryBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    deadline: Optional[date] = Field(None, example="2025-02-10") #підказка як в swagger вводити дату 
    

class TaskCreate(TaskBase):    
    status: Literal["new", "in_progress", "done"] = "new"
    
class TaskStatusUpdate(BaseModel):
    status: Literal["new", "in_progress", "done"] 


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[Literal["new", "in_progress", "done"]] = None
    deadline: Optional[date] = None   


class Task(TaskBase):
    id: int
    status: str
    category_id: int
    user_id: int
    created_at: datetime
    updated_at: datetime 
    model_config = ConfigDict(from_attributes=True)
    

# Для виведення всіх завдань з фільтром
class TaskGroups(BaseModel):
    all: List[Task]
    new: List[Task]
    in_progress: List[Task]
    done: List[Task]
    by_deadline: Optional[List[Task]] = None
    by_status: Optional[List[Task]] = None
    by_deadline_and_status: Optional[List[Task]] = None
    model_config = ConfigDict(from_attributes=True)


class DeletedCategory(BaseModel):
    deleted_category: Category
    deleted_tasks: List[Task]


class DeletedTasks(BaseModel):
    deleted_tasks: List[Task]
    
    
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
