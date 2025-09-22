import sys
import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# Додаємо корінь проєкту в sys.path,щоб app був видимим
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Alembic config
config = context.config
fileConfig(config.config_file_name)

target_metadata = None
_DB_MODULE = None
_db_url = None

# імпортуємо з арр або з кореня
try:
    import app.database as _DB_MODULE
    import app.models  
    target_metadata = _DB_MODULE.Base.metadata
    if hasattr(_DB_MODULE, "SQLALCHEMY_DATABASE_URL"):
        _db_url = _DB_MODULE.SQLALCHEMY_DATABASE_URL
    elif hasattr(_DB_MODULE, "engine"):
        _db_url = str(_DB_MODULE.engine.url)
except Exception:
    try:
        import database as _DB_MODULE
        import models
        target_metadata = _DB_MODULE.Base.metadata
        if hasattr(_DB_MODULE, "SQLALCHEMY_DATABASE_URL"):
            _db_url = _DB_MODULE.SQLALCHEMY_DATABASE_URL
        elif hasattr(_DB_MODULE, "engine"):
            _db_url = str(_DB_MODULE.engine.url)
    except Exception as exc:
        raise ImportError(
            "Не вдалося імпортувати database/Base або models. "
            "Перевір структуру проєкту і наявність app/__init__.py. "
            f"Оригінальна помилка: {exc}"
        )

# Якщо змінна url знайдена у database.py — підставляємо її в alembic config
if _db_url:
    config.set_main_option("sqlalchemy.url", _db_url)

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
