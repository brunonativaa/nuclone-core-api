import os
from typing import AsyncGenerator
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

# 1. Carrega as variáveis do arquivo .env PRIMEIRO
load_dotenv()

# 2. Garante driver assíncrono (postgresql+asyncpg://) na URL de conexão
DEFAULT_DB_URL = "postgresql://postgres:postgrespassword@localhost:5432/core_banking"
RAW_DATABASE_URL = os.getenv("DATABASE_URL") or DEFAULT_DB_URL

# Converte URLs 'postgresql://' padrão para o driver assíncrono 'postgresql+asyncpg://' se necessário
if RAW_DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = RAW_DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)
elif RAW_DATABASE_URL.startswith("postgresql+psycopg2://"):
    DATABASE_URL = RAW_DATABASE_URL.replace("postgresql+psycopg2://", "postgresql+asyncpg://", 1)
else:
    DATABASE_URL = RAW_DATABASE_URL

engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # Ativa logs detalhados de SQL para depuração
    future=True,  # Usa a API futura do SQLAlchemy
)

AsycSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,# Usa sessões assíncronas
    expire_on_commit=False,  # Evita expiração automática de objetos após commit
    autoflush=False,  # Desativa flush automático para maior controle
)
# 5. Base Declarativa Moderna (SQLAlchemy 2.0 style)
class Base(DeclarativeBase):
    pass

# 6. Gerador de Sessão Injetável para FastAPI (expõe tanto get_db quanto get_db_session)
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsycSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

# para manter compatibilidade com módulos antigos que importam 'get_db'
get_db = get_db_session