import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.database import SessionLocal
from app import crud

db = SessionLocal()

# Припустимо, хочемо видалити завдання з id=9
task_id = 9
deleted_task = crud.delete_task(db, task_id=task_id)

if deleted_task:
    print(f"Task {task_id} deleted successfully")
else:
    print(f"Task {task_id} not found")

db.close()
