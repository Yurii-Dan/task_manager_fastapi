from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Literal
from datetime import date

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
    deadline: Optional[date] = None   


class TaskCreate(TaskBase):
    category_id: int 
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
    model_config = ConfigDict(from_attributes=True)


class DeletedCategory(BaseModel):
    deleted_category: Category
    deleted_tasks: List[Task]


class DeletedTasks(BaseModel):
    deleted_tasks: List[Task]
