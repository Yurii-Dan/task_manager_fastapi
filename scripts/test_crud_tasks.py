import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.database import SessionLocal
from app import crud

db = SessionLocal()
tasks_dict = crud.get_tasks(db)
# Всі завдання
print("All tasks:")
for t in tasks_dict["all"]:
    print(t.id, t.title, t.is_done)

# Тільки виконані
print("\nDone tasks:")
for t in tasks_dict["completed"]:
    print(t.id, t.title, t.is_done)

# Тільки невиконані
print("\nNot done tasks:")
for t in tasks_dict["unfulfilled"]:
    print(t.id, t.title, t.is_done)



db.close()
