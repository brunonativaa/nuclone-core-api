import os
from functools import lru_cache

class Settings:
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "nuclone_db")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "database")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")
    SECRET_KEY: str = os.getenv("SECRET_KEY" ,"chave_secreta_padrao_para_testes_unitarios_123")
    
    # Utiliza o driver asyncpg para suporte I/O assíncrono do SQLAlchemy
    DATABASE_URL: str = (
        f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@"
        f"{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )


    RABBITMQ_USER: str = os.getenv("RABBITMQ_USER", "admin")
    RABBITMQ_PASSWORD: str = os.getenv("RABBITMQ_PASSWORD", "admin123")
    RABBITMQ_HOST: str = os.getenv("RABBITMQ_HOST", "localhost")
    RABBITMQ_PORT: str = os.getenv("RABBITMQ_PORT", "5672")
    
    # Monta a URL que o broker.py está tentando acessar
    RABBITMQ_URL: str = (
        f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@"
        f"{RABBITMQ_HOST}:{RABBITMQ_PORT}/"
    )


@lru_cache()
def get_settings() -> Settings:
    return Settings()