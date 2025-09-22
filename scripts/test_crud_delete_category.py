import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.database import SessionLocal
from app import crud

db = SessionLocal()
#видаляємо 6 категорію
category_id = 7
deleted_category = crud.delete_category(db, category_id=category_id)

if deleted_category:
    print(f"Category {category_id} and its tasks deleted successfully")
else:
    print(f"Category {category_id} not found")

db.close()
