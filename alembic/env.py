import os
import sys
from os.path import abspath, dirname
from dotenv import load_dotenv
from alembic import context

# 1. Ajusta o caminho do sys.path ANTES de qualquer import do projeto
sys.path.insert(0, dirname(dirname(abspath(__file__))))

# 2. Carrega as variáveis de ambiente
load_dotenv()

DEFAULT_DB_URL = "postgresql://postgres:postgrespassword@localhost:5432/core_banking"
DATABASE_URL = os.getenv("DATABASE_URL") or DEFAULT_DB_URL

# 3. Configura a URL da base de dados no Alembic
config = context.config
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# 4. Importa a Base declarada no Core da aplicação
from src.core.database import Base  # noqa: E402

# 5. Importa TODOS os modelos registrados para que o Base.metadata reconheça o Schema completo
from src.modules.account.model import ContaModel, SaldoContaModel  # noqa: E402
from src.modules.ledger.model import TransacaoModel  # noqa: E402
from src.modules.customer.model import ClienteModel, EnderecoModel, TelefoneModel  # noqa: E402
from src.modules.pix.model import ChavePixModel  # noqa: E402
from src.modules.limits.model import LimiteContaModel  # noqa: E402

# 6. Associa os Metadados unificados para o --autogenerate
target_metadata = Base.metadata