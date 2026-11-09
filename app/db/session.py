# app/db/session.py

from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.core.config import settings

# 1. Cria o motor de conexão do SQLAlchemy apontando para a DATABASE_URL do .env
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True  # Verifica se a conexão com o PostgreSQL continua viva antes de executar queries
)

# 2. Fábrica de sessões para gerenciar transações com o banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# 3. Classe Base declarativa usada por todos os modelos (User, Client, Lead)
class Base(DeclarativeBase):
    pass


# 4. Injeção de Dependência para o FastAPI (fornece uma sessão por requisição)
def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()