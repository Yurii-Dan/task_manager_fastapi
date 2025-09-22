# Task Manager FastAPI

**Status:** In development

## Description
A simple task manager API built with FastAPI. Each task can belong to a category. Supports CRUD operations for tasks and categories.

## Technologies
- Python 3.13
- FastAPI
- SQLAlchemy
- Alembic
- SQLite
- Pydantic

## Setup
1. Create a virtual environment and activate it.
2. Install dependencies: `pip install -r requirements.txt`
3. Run Alembic migrations: `alembic upgrade head`
4. Start the app: `uvicorn app.main:app --reload`

## Notes
- Database file: `my_task.db` (SQLite)
- API is still under development.
