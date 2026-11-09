# migrations/env.py

import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# 1. Adiciona a raiz do projeto (C:\flowcrm-backend) ao caminho do Python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 2. Importa as configurações do .env e a Base com os modelos registrados
from app.core.config import settings
from app.db.session import Base
import app.models  # Carrega os modelos User, Client e Lead no Alembic # noqa: F401

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Define o metadata onde o Alembic buscará as tabelas mapeadas
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Executa migrações no modo 'offline' (gerando apenas o script SQL)."""
    url = settings.DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Executa migrações no modo 'online' (conectando direto ao PostgreSQL)."""
    # Injeta a DATABASE_URL dinâmica vinda do arquivo .env
    configuration = config.get_section(config.config_ini_section) or {}
    configuration["sqlalchemy.url"] = settings.DATABASE_URL
    
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
