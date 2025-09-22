import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.database import SessionLocal
from app import crud

db = SessionLocal()

# Припустимо, ми хочемо оновити завдання з id=9
task_id = 9
updated_task = crud.update_task_status(db, task_id=task_id, is_done=True)

print(f"Task {updated_task.id} - {updated_task.title} status updated to {updated_task.is_done}")

db.close()
