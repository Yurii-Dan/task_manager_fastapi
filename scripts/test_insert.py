import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.database import SessionLocal
from app import models

db = SessionLocal()

# Додати нову категорію
new_category = models.Category(name="Learning")
db.add(new_category)
db.commit()
db.refresh(new_category)
print(f"Category created: {new_category.id} - {new_category.name}")

# Додати нове завдання в цю категорію
new_task = models.Task(title="Learn FastAPI", description="Practice CRUD", category_id=new_category.id)
db.add(new_task)
db.commit()
db.refresh(new_task)
print(f"Task created: {new_task.id} - {new_task.title} (Category {new_task.category_id})")

db.close()
