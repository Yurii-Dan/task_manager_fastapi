from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import engine, SessionLocal, Base
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


# Отримання списку завдань (з фільтром: всі, тільки виконані, тільки невиконані)
@app.get("/tasks/", response_model=schemas.TaskList)
def get_tasks(db: Session = Depends(get_db)):
    return crud.get_tasks(db=db)
# Створення завдання
@app.post("/tasks/{category_id}", response_model=schemas.Task) 
def create_task(task: schemas.TaskCreate, category_id: int, db: Session = Depends(get_db)):
    return crud.create_task(db=db, task=task, category_id=category_id)
# Оновлення is_done (виконане чи не виконане завдання)
@app.put("/tasks/{task_id}", response_model=schemas.Task)
def update_task_status(task_id: int, update:schemas.TaskUpdate, db: Session = Depends(get_db)):
    return crud.update_task_status(db=db, task_id=task_id, is_done=update.is_done)
# Видалення завдання (або всіх завдань для певної категорії)
@app.delete("/tasks/", response_model=schemas.DeletedTasks)
def delete_task(
    task_id: int | None = Query(default=None),
    category_id: int | None = Query(default=None),
    db: Session = Depends(get_db)
):
    return crud.delete_task(db=db, task_id=task_id, category_id=category_id)

