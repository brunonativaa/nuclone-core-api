import os
from typing import AsyncGenerator
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

load_dotenv()

DEFAULT_DB_URL = "postgresql://postgres:postgrespassword@localhost:5432/core_banking"
RAW_DATABASE_URL = os.getenv("DATABASE_URL") or DEFAULT_DB_URL

if RAW_DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = RAW_DATABASE_URL.replace(
        "postgresql://", "postgresql+asyncpg://", 1)
elif RAW_DATABASE_URL.startswith("postgresql+psycopg2://"):
    DATABASE_URL = RAW_DATABASE_URL.replace(
        "postgresql+psycopg2://", "postgresql+asyncpg://", 1)
else:
    DATABASE_URL = RAW_DATABASE_URL

engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    future=True,
)

# CORRIGIDO: de AsycSessionLocal para AsyncSessionLocal (com 'n')
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


class Base(DeclarativeBase):
    pass


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

get_db = get_db_session
