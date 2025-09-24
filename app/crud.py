from sqlalchemy.orm import Session
from . import models, schemas
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
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
    

# Отримання списку завдань (з фільтром: всі, тільки виконані, тільки невиконані)
def get_tasks(db: Session):
    return {
        "all": db.query(models.Task).all(),
        "completed": db.query(models.Task).filter(models.Task.is_done == True).all(),
        "unfulfilled": db.query(models.Task).filter(models.Task.is_done == False).all()
    }

# Створення завдання
def create_task(db: Session, task: schemas.TaskCreate, category_id: int):
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not category:
         raise HTTPException(status_code=404, detail="Category not found")
    db_task = models.Task(title=task.title,description=task.description, category_id=category_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

# Оновлення is_done (виконане чи не виконане завдання)
def update_task_status(db: Session, task_id: int, is_done: bool):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.is_done = is_done
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