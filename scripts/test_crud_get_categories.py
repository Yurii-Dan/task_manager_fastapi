import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.database import SessionLocal
from app import crud

db = SessionLocal()

# Отримати всі категорії
categories = crud.get_categories(db)
for cat in categories:
    print(cat.id, cat.name)

db.close()
