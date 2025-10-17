import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.database import SessionLocal
from app import crud

db = SessionLocal()

#Видаляємо завдання з id=7
task_id = 7
deleted_task = crud.delete_task(db, task_id=task_id)

if deleted_task:
    print(f"Task {task_id} deleted successfully")
else:
    print(f"Task {task_id} not found")

db.close()
