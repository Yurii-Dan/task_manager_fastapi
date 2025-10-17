import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.database import SessionLocal
from app import crud, schemas

db = SessionLocal()

# Оновлюємо завдання з id=7
task_id = 7

# Створюємо Pydantic-схему
task_update = schemas.TaskUpdate(title="repetition of the task", status="in_progress")

#Викликаємо функцію оновлення завдання
updated_task = crud.update_task(db, task_id=task_id, task_update=task_update)

print(f"Task {updated_task.id} - {updated_task.title} status updated to {updated_task.status}")

db.close()
