import os

class Settings:
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "nuclone_db")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "database")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "bdsovijrkldlhrgejnds mklcjkdfdserg")
    
    # Utiliza o driver asyncpg para suporte I/O assíncrono do SQLAlchemy
    DATABASE_URL: str = (
        f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@"
        f"{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )

# Instância exportada para ser importada no security.py e database.py
settings = Settings()