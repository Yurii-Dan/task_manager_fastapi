import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.database import SessionLocal
from app import crud

db = SessionLocal()
tasks_dict = crud.get_tasks(db)
# Всі завдання
print("All tasks:")
for t in tasks_dict["all"]:
    print(t.id, t.title, t.status, t.deadline)

# Тільки нові
print("\nnew:")
for t in tasks_dict["new"]:
    print(t.id, t.title, t.status, t.deadline)

# Тільки в процесі
print("\nin_progress:")
for t in tasks_dict["in_progress"]:
    print(t.id, t.title, t.status, t.deadline)

# Тільки виконані
print("\ndone:")
for t in tasks_dict["done"]:
    print(t.id, t.title, t.status, t.deadline)

db.close()
