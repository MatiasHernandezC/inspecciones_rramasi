from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Importar tu Base
from ..app.db.base_class import Base  # Aquí está tu declarative_base con todos los modelos

# Config Alembic
config = context.config

# Si existe fileConfig, carga el logging de alembic.ini
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata de tus modelos
target_metadata = Base.metadata

# Construir la URL desde .env
def get_url():
    user = os.getenv("POSTGRES_USER", "postgres")
    password = os.getenv("POSTGRES_PASSWORD", "postgres")
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5432")
    db = os.getenv("POSTGRES_DB", "inspecciones_db")
    return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"

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
