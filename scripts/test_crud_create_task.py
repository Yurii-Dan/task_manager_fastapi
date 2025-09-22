import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.database import SessionLocal
from app import crud, schemas

db = SessionLocal()

# Створюємо Pydantic-схему
task_data = schemas.TaskCreate(title="Prepare presentation")

# Викликаємо функцію create_task
new_task = crud.create_task(db, task=task_data, category_id=1)
print(f"Task created: {new_task.id} - {new_task.title} (Category {new_task.category_id})")

db.close()

