from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import os

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from api.core.config import settings
from api.core.supabase_client import metadata

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL) 

# Interpret the config file for Python logging.
fileConfig(config.config_file_name)

# Import your models here and set target_metadata
# Example:
# from api.models import Base
# target_metadata = Base.metadata
target_metadata = metadata  # Substitua por sua metadata, se necessário

def get_url():
    return settings.DATABASE_URL

def run_migrations_offline():
    url = get_url()
    context.configure(
        url=url, 
        target_metadata=target_metadata, 
        literal_binds=True, 
        compare_type=True,
        # dialect_opts={"paramstyle": "named"}
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
        context.configure(
            connection=connection, target_metadata=target_metadata, compare_type=True
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
