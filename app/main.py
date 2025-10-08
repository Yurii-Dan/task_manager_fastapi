from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import engine, SessionLocal, Base
from datetime import date
from typing import Literal, Optional
# Створюємо таблиці
#Base.metadata.create_all(bind=engine)  

app = FastAPI()

# Залежність: отримаємо сесію БД для кожного запиту
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
# Отримання списку категорій
@app.get("/categories/", response_model=list[schemas.Category])
def get_categories(db: Session = Depends(get_db)):
    return crud.get_categories(db=db)

# Створення категорії
@app.post("/categories/", response_model=schemas.Category) 
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    return crud.create_category(db=db, category=category)

#Видалення категорії разом з завданням
@app.delete("/categories/{category_id}", response_model=schemas.DeletedCategory)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    return crud.delete_category(db=db, category_id=category_id)


# Отримання списку завдань з фільтром
@app.get("/tasks/", response_model=schemas.TaskGroups)
def get_tasks(
    db: Session = Depends(get_db),
    status: Optional[Literal["new", "in_progress", "done"]] = Query(None),
    deadline: Optional[date] = Query(None, example="2025-02-10")
):
    return crud.get_tasks(db=db, status=status, deadline=deadline)


# Створення завдання
@app.post("/tasks/{category_id}", response_model=schemas.Task) 
def create_task(task: schemas.TaskCreate, category_id: int, db: Session = Depends(get_db)):
    return crud.create_task(db=db, task=task, category_id=category_id)

# Оновлення status
@app.patch("/tasks/{task_id}/status", response_model=schemas.Task)
def update_task_status(task_id: int, task_update: schemas.TaskStatusUpdate, db: Session = Depends(get_db)):
    """
    Оновлення статусу завдання.
    Можливі значення статусу: `"new"`, `"in_progress"`, `"done"`.
    """
    return crud.update_task_status(db, task_id=task_id, status=task_update.status)

# Оновлення завдання
@app.patch("/tasks/{task_id}",response_model=schemas.Task)
def update_task(task_id:int, task_update: schemas.TaskUpdate,db: Session = Depends(get_db)):
    return crud.update_task(db, task_id=task_id, task_update=task_update)

# Видалення завдання (або всіх завдань для певної категорії)
@app.delete("/tasks/", response_model=schemas.DeletedTasks)
def delete_task(
    task_id: int | None = Query(default=None),
    category_id: int | None = Query(default=None),
    db: Session = Depends(get_db)
):
    return crud.delete_task(db=db, task_id=task_id, category_id=category_id)

