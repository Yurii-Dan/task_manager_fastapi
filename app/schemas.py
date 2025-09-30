from pydantic import BaseModel, ConfigDict
from typing import Optional, List
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


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
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
