import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.database import SessionLocal
from app import crud, schemas
from sqlalchemy.exc import IntegrityError

db = SessionLocal()

category_name = "Books"
category_data = schemas.CategoryCreate(name=category_name)

try:
    new_category = crud.create_category(db, category=category_data)
    print(f"Category created via CRUD: {new_category.id} - {new_category.name}")
except IntegrityError:
    db.rollback()
    print(f"Category '{category_name}' already exists in the database.")

db.close()
