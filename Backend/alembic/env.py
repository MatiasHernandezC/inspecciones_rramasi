from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import load_dotenv
import os, sys

# Add backend folder to sys.path (two levels up from this file)
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))  # .../backend
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

load_dotenv(os.path.join(PROJECT_ROOT, ".env"))

# Import Base with models imported so Alembic can see tables
from app.models import Base

config = context.config


def get_url():
    user = os.getenv("POSTGRES_USER", "postgres")
    password = os.getenv("POSTGRES_PASSWORD", "postgres")
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5432")
    db = os.getenv("POSTGRES_DB", "inspecciones_db")
    return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"


target_metadata = Base.metadata

# Configure logging from alembic.ini if present
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


def run_migrations_offline():
    url = get_url()
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True, dialect_opts={"paramstyle": "named"}
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    url = get_url()
    connectable = engine_from_config(
        {"sqlalchemy.url": url},
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

