
from src.modules.account.model import ContaModel, SaldoContaModel, TransacaoModel
from src.modules.customer.model import ClienteModel, EnderecoModel, TelefoneModel
import os
import sys
from os.path import abspath, dirname
from dotenv import load_dotenv
from alembic import context

# 1. PRIMEIRO: Ajusta o caminho de importação (deve vir ANTES de qualquer import do projeto)
sys.path.insert(0, dirname(dirname(abspath(__file__))))

# 2. Carrega as variáveis de ambiente
load_dotenv()

DEFAULT_DB_URL = "postgresql://postgres:postgrespassword@localhost:5432/core_banking"
DATABASE_URL = os.getenv("DATABASE_URL") or DEFAULT_DB_URL

# 3. Injeta a URL na configuração do Alembic
config = context.config
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# 4. SEGUNDO: Imports da Base e dos Models (DEPOIS do sys.path e do load_dotenv)
from src.core.database import Base  # noqa: E402
from src.modules.pix.model import KeyPixModel  # noqa: E402


# 5. Associa a Base para o autogenerate
target_metadata = Base.metadata
