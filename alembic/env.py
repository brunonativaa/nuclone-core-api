import asyncio
import os
import sys
from logging.config import fileConfig

from alembic import context
from sqlalchemy.ext.asyncio import create_async_engine

# 1. Garante que o diretório raiz do projeto está no path do Python
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 2. Importa a Base e todos os Models da aplicação para o target_metadata reconhecer o esquema
from src.core.database import Base  # noqa: E402
from src.modules.account.model import ContaModel, SaldoContaModel  # noqa: E402
from src.modules.customer.model import ClienteModel, EnderecoModel, TelefoneModel  # noqa: E402
from src.modules.ledger.model import TransacaoModel  # noqa: E402
from src.modules.limits.model import LimiteContaModel  # noqa: E402
from src.modules.pix.model import ChavePixModel  # noqa: E402

# Configuração de logging do Alembic
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Define o metadata alvo para o autogenerate
target_metadata = Base.metadata

# Obtém a URL do banco diretamente das variáveis de ambiente ou do .env
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://dev_bruno:2586mypass2031@nuclone-postgres:5432/nuclone_db",
)
config.set_main_option("sqlalchemy.url", DATABASE_URL)


def run_migrations_offline() -> None:
    """Executa migrações no modo 'offline'."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Cria uma engine assíncrona e executa as migrações usando run_sync."""
    connectable = create_async_engine(
        config.get_main_option("sqlalchemy.url"),
        future=True,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Executa migrações no modo 'online' (assíncrono)."""
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()