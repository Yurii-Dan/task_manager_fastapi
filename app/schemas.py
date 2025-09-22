from pydantic import BaseModel, ConfigDict
from typing import Optional, List

class Category(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)
    
class Task(BaseModel):
    id: int
    title: str 
    description: Optional[str] = None
    is_done: bool  
    category_id: Optional[int] = None
    model_config = ConfigDict(from_attributes=True)

class CategoryCreate(BaseModel):
    name: str

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None

class TaskList(BaseModel):
    all: list[Task]
    completed: list[Task]
    unfulfilled: list[Task]

class TaskUpdate(BaseModel):
    is_done: bool

class DeletedCategory(BaseModel):
    deleted_category: Category
    deleted_tasks: list[Task]

class DeletedTasks(BaseModel):
    deleted_tasks: list[Task]
