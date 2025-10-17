import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.database import SessionLocal
from app import crud

db = SessionLocal()

# Припустимо, ми хочемо оновити завдання з id=7
task_id = 7
updated_task = crud.update_task_status(db, task_id=task_id, status="done")

print(f"Task {updated_task.id} - {updated_task.title} status updated to {updated_task.status}")

db.close()
