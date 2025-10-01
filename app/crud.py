from sqlalchemy.orm import Session
from . import models, schemas
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from datetime import date
from typing import Literal
# Отримання списку категорій
def get_categories(db: Session):
    return db.query(models.Category).all()
# Створення категорії
def create_category(db: Session, category: schemas.CategoryCreate):
    db_category = models.Category(name=category.name)
    db.add(db_category)
    try:
        db.commit()
        db.refresh(db_category)
        return db_category
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Category already exists")
# Видалення категорії разом з завданнями
def delete_category(db: Session, category_id: int):
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not category: raise HTTPException(status_code=404, detail="Category not found")
    tasks = db.query(models.Task).filter(models.Task.category_id == category_id).all()              
    if tasks:
        for task in tasks:
            db.delete(task)
    db.delete(category)
    db.commit()
    return {"deleted_category": category, "deleted_tasks": tasks}
    

# Отримання списку завдань з фільтрами: всі, нові, в процесі, завершені, по даті
def get_tasks(db: Session, deadline: date = None, status: Literal["new", "in_progress", "done"] = None):
    tasks = {
        "all": db.query(models.Task).all(),
        "new": db.query(models.Task).filter(models.Task.status == "new").all(),
        "in progress": db.query(models.Task).filter(models.Task.status == "in_progress").all(),
        "done": db.query(models.Task).filter(models.Task.status == "done").all(),
    }

    if deadline:
        tasks[f"on date {deadline}"] = db.query(models.Task).filter(models.Task.deadline == deadline).all()
    if status:
        tasks[f"by status: {status}"] = db.query(models.Task).filter(models.Task.status == status).all()
    if deadline and status:
        tasks[f"on {deadline} & status: {status}"] = db.query(models.Task).filter(
            models.Task.deadline == deadline,
            models.Task.status == status
        ).all()

    return tasks

# Створення завдання
def create_task(db: Session, task: schemas.TaskCreate):
    category = db.query(models.Category).filter(models.Category.id == task.category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    db_task = models.Task(
        title=task.title,
        description=task.description,
        category_id=task.category_id,
        status=task.status,
        deadline=task.deadline
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


# Оновлення status
def update_task_status(db: Session, task_id: int, status:str):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.status = status
    db.commit()
    db.refresh(task)
    return task

# Оновлення завдання (task)
def update_task(db: Session, task_id: int, task_update: schemas.TaskUpdate):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Оновлюємо тільки передані поля
    if task_update.title is not None:
        task.title = task_update.title
    if task_update.description is not None:
        task.description = task_update.description
    if task_update.status is not None:
        task.status = task_update.status
    if task_update.deadline is not None:
        task.deadline = task_update.deadline

    db.commit()
    db.refresh(task)
    return task

# Видалення завдання (або всіх завдань для певної категорії)
def delete_task(db: Session, task_id: int = None, category_id: int = None):
    if task_id:
        task = db.query(models.Task).filter(models.Task.id == task_id).first()
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        db.delete(task)
        db.commit()
        return {"deleted_tasks": [task]} 

    if category_id:
        tasks = db.query(models.Task).filter(models.Task.category_id == category_id).all()
        if not tasks:
            raise HTTPException(status_code=404, detail="No tasks for this category")
        for t in tasks:
            db.delete(t)
        db.commit()
        return {"deleted_tasks": tasks}

    raise HTTPException(status_code=400, detail="Provide either task_id or category_id")