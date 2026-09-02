import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# 1. Carrega as variáveis do arquivo .env PRIMEIRO
load_dotenv()

# 2. Garante fallback caso a variável VENHA VAZIA ("") ou seja NULA (None)
DEFAULT_DB_URL = "postgresql://postgres:postgrespassword@localhost:5432/nuclone_db"
DATABASE_URL = os.getenv("DATABASE_URL") or DEFAULT_DB_URL

# 3. Cria a engine com a URL tratada
engine = create_engine(DATABASE_URL, echo=True, future=True)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    future=True
)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
