from src.modules.account.model import ContaModel
from src.modules.customer.model import ClienteModel
from src.modules.pix.model import TypeChaveEnum, KeyPixModel
from src.core.database import Base
import os
import sys
from os.path import abspath, dirname
from dotenv import load_dotenv
from alembic import context

# 1. Configura o sys.path PRIMEIRO para permitir imports do 'src'
sys.path.insert(0, dirname(dirname(abspath(__file__))))

# 2. Carrega as variáveis de ambiente do .env local (se existir)
load_dotenv()

# 3. Garante um fallback seguro para a DATABASE_URL caso a ENV esteja vazia
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgrespassword@localhost:5432/nuclone_db"
)

# 4. Configura a URL no Alembic ANTES de importar os models/database
config = context.config
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# 5. AGORA SIM importa os Models e a Base com o caminho e a URL já ajustados

target_metadata = Base.metadata

print("--- TABELAS MAPEADAS NO ALEMBIC ---")
print(list(target_metadata.tables.keys()))
print("----------------------------------")
