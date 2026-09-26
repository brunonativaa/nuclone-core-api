import os 

os.environ["DATABASE_URL"] = "sqlite:///:memory:"


from datetime import date, datetime, timezone
import uuid
import pytest
import sqlalchemy
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.main import app
from src.core.database import get_db, Base
from src.modules.account.model import ContaModel, SaldoContaModel
from src.modules.customer.model import ClienteModel
from src.modules.pix.model import ChavePixModel


# -----------------------------------------------------------------------------
# Configuração do Banco de Dados SQLite em Memória para Testes
# -----------------------------------------------------------------------------

TEST_DATABASE_URL = "sqlite:///:memory:"

# StaticPool e check_same_thread=False mantêm a mesma conexão em memória para o ciclo do teste
test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

@pytest.fixture(scope="session", autouse=True)
def setup_db():
    """Cria as tabelas em memória no início do suite e descarta ao final."""
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def db_session():  
    """Fornece uma sessão isolada com suporte a rollback por teste."""
    connection = test_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    nested = connection.begin_nested()

    @sqlalchemy.event.listens_for(session, "after_transaction_end")
    def restart_savepoint(session, transaction):
        nonlocal nested
        if not nested.is_active:
            nested = connection.begin_nested()

    yield session

    session.close()
    transaction.rollback()
    connection.close()



@pytest.fixture
def client(db_session):
    """Substitui a dependência get_db do FastAPI pela sessão de testes."""
    def _override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = _override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()

# -----------------------------------------------------------------------------
# Fixtures de Dados de Teste (Massa de Dados)
# -----------------------------------------------------------------------------

@pytest.fixture
def chave_pix_destino(db_session, id_conta_destino):
    chave = ChavePixModel(
        id_conta=id_conta_destino,
        tipo_chave="EMAIL",
        valor_chave="destino@email.com"
    )
    db_session.add(chave)
    db_session.flush()  # Usar flush em vez de commit para não estourar o Savepoint
    return chave.valor_chave


@pytest.fixture
def chave_pix_origem(db_session, id_conta_origem):
    chave = ChavePixModel(
        id_conta=id_conta_origem,
        tipo_chave="EMAIL",
        valor_chave="origem@email.com"
    )
    db_session.add(chave)
    db_session.flush()  # Usar flush em vez de commit para não estourar o Savepoint
    return chave.valor_chave


@pytest.fixture
def valid_customer_data():
    uid = str(uuid.uuid4())[:8]
    return {
        "nome": f"Bruno Teste {uid}",
        "cpf": str(uuid.uuid4().int)[:11].zfill(11),
        "email": f"pytest_{uid}@email.com",
        "senha_hash": "senha_segura_test",
        "pin_transacao_hash": "1234",
        "sexo": "M",
        "data_nascimento": date(1997, 8, 15)
    }


@pytest.fixture
def id_conta_origem(db_session, valid_customer_data):
    cliente = ClienteModel(**valid_customer_data)
    db_session.add(cliente)
    db_session.flush()

    uid = str(uuid.uuid4())[:5]
    conta = ContaModel(
        id_cliente=cliente.id_cliente,
        num_conta=f"000{uid}-1",
        agencia="0001",
        tipo_conta="PF"
    )
    db_session.add(conta)
    db_session.flush()

    saldo = SaldoContaModel(
        id_conta=conta.id_conta,
        saldo_disponivel=100.00,
        saldo_bloqueado=0.00,
        ultima_atualizacao=datetime.now(timezone.utc)
    )
    db_session.add(saldo)
    db_session.flush()

    return conta.id_conta


@pytest.fixture
def id_conta_destino(db_session):
    uid = str(uuid.uuid4())[:8]
    dados_destino = {
        "nome": "Cliente Destino Teste",
        "cpf": f"{uuid.uuid4().int}"[:11],
        "email": f"destino_{uid}@email.com",
        "senha_hash": "senha_segura_test",
        "pin_transacao_hash": "1234",
        "sexo": "F",
        "data_nascimento": date(1998, 1, 1)
    }
    cliente = ClienteModel(**dados_destino)
    db_session.add(cliente)
    db_session.flush()

    conta = ContaModel(
        id_cliente=cliente.id_cliente,
        num_conta=f"000{uid[:5]}-2",
        agencia="0001",
        tipo_conta="PF"
    )
    db_session.add(conta)
    db_session.flush()

    saldo = SaldoContaModel(
        id_conta=conta.id_conta,
        saldo_disponivel=0.00,
        saldo_bloqueado=0.00,
        ultima_atualizacao=datetime.now(timezone.utc)
    )
    db_session.add(saldo)
    db_session.flush()

    return conta.id_conta

@pytest.fixture
def chave_pix_origem(db_session, id_conta_origem):
    chave = ChavePixModel(
        id_conta=id_conta_origem,
        tipo_chave="EMAIL",
        valor_chave="origem@email.com"
    )
    db_session.add(chave)
    db_session.flush()
    return chave.valor_chave

@pytest.fixture
def chave_pix_destino(db_session, id_conta_destino):
    chave = ChavePixModel(
        id_conta=id_conta_destino,
        tipo_chave="EMAIL",
        valor_chave="destino@email.com"
    )
    db_session.add(chave)
    db_session.flush()
    return chave.valor_chave
