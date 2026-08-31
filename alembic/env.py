from src.modules.pix.model import TypeChaveEnum, KeyPixModel
from src.modules.customer.model import ClienteModel
from src.modules.account.model import ContaModel
from src.core.database import Base
from alembic import context
import sys
import os
from os.path import abspath, dirname
from dotenv import load_dotenv

# 1. Carrega as variáveis do arquivo .env localizado na raiz
load_dotenv()

# 2. Adiciona o diretório raiz do projeto ao sys.path
sys.path.insert(0, dirname(dirname(abspath(__file__))))


# Importe sua Base e os Models

target_metadata = Base.metadata

print("--- TABELAS MAPEADAS NO ALEMBIC ---")
print(list(target_metadata.tables.keys()))
print("----------------------------------")

# Configuração do Alembic
config = context.config

# 3. Sobrescreve a URL do alembic.ini com a variável DATABASE_URL do .env
database_url = os.getenv("DATABASE_URL")
if database_url:
    config.set_main_option("sqlalchemy.url", database_url)

# ... Mantenha o restante do código padrão do env.py abaixo ...
