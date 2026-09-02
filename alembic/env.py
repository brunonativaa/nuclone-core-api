from src.modules.pix.model import KeyPixModel
from src.modules.account.model import ContaModel, SaldoContaModel, TransacaoModel
from src.modules.customer.model import ClienteModel, EnderecoModel, TelefoneModel
from src.core.database import Base
import os
import sys
from os.path import abspath, dirname
from dotenv import load_dotenv
from alembic import context

# 1. Ajusta o caminho de importação
sys.path.insert(0, dirname(dirname(abspath(__file__))))

# 2. Carrega as variáveis de ambiente
load_dotenv()

DEFAULT_DB_URL = "postgresql://postgres:postgrespassword@localhost:5432/nuclone_db"
DATABASE_URL = os.getenv("DATABASE_URL") or DEFAULT_DB_URL

# 3. Injeta a URL no Alembic
config = context.config
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# 4. Imports dos Models para registrar no Metadata

target_metadata = Base.metadata
