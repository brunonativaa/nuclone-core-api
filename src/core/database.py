import os
from typing import AsyncGenerator
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.pool import StaticPool

load_dotenv()

DEFAULT_DB_URL = "postgresql://postgres:postgrespassword@localhost:5432/core_banking"
RAW_DATABASE_URL = os.getenv("DATABASE_URL") or DEFAULT_DB_URL

# Garantia do driver assíncrono para PostgreSQL
if RAW_DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = RAW_DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)
elif RAW_DATABASE_URL.startswith("postgresql+psycopg2://"):
    DATABASE_URL = RAW_DATABASE_URL.replace("postgresql+psycopg2://", "postgresql+asyncpg://", 1)
else:
    DATABASE_URL = RAW_DATABASE_URL

# Configurações dinâmicas de Engine para suporte a Postgres e SQLite (Pytest)
engine_kwargs = {"echo": True, "future": True}

if DATABASE_URL.startswith("sqlite"):
    engine_kwargs.update({
        "connect_args": {"check_same_thread": False},
        "poolclass": StaticPool
    })

engine = create_async_engine(DATABASE_URL, **engine_kwargs)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


class Base(DeclarativeBase):
    pass


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency Injection do FastAPI para fornecer sessões de banco de dados."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

#  compatibilidade  injeção de dependência nas rotas
get_db = get_db_session