import datetime
import uuid
import pytest
from fastapi.testclient import TestClient

from src.main import app
# Importa diretamente a instância do engine do core do projeto
from src.core.database import engine, SessionLocal, get_db, Base
from src.modules.account.model import ContaModel, SaldoContaModel
from src.modules.customer.model import ClienteModel
from src.modules.pix.model import KeyPixModel


@pytest.fixture(scope="session")
def setup_db():
    """Cria as tabelas apenas quando o banco for realmente necessário."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session(setup_db):  # Passa o setup_db como dependência aqui
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionLocal(bind=connection)

    session.begin_nested()

    @pytest.hookimpl(tryfirst=True)
    def on_rollback():
        session.begin_nested()

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(db_session):
    def _override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = _override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def chave_pix_destino(db_session, id_conta_destino):
    chave = KeyPixModel(
        id_conta=id_conta_destino,
        tipo_chave="EMAIL",
        valor_chave="destino@email.com"
    )
    db_session.add(chave)
    db_session.flush()  # Usar flush em vez de commit para não estourar o Savepoint
    return chave.valor_chave


@pytest.fixture
def chave_pix_origem(db_session, id_conta_origem):
    chave = KeyPixModel(
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
        "cpf": f"{uuid.uuid4().int}"[:11],
        "email": f"pytest_{uid}@email.com",
        "senha": "senha_segura_test",
        "sexo": "M",
        "data_nascimento": "1997-08-15"
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
        ultima_atualizacao=datetime.datetime.now(datetime.timezone.utc)
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
        "senha": "senha_segura_test",
        "sexo": "F",
        "data_nascimento": "1998-01-01"
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
        saldo_disponivel=0,
        saldo_bloqueado=0,
        ultima_atualizacao=datetime.datetime.now(datetime.timezone.utc)
    )
    db_session.add(saldo)
    db_session.flush()

    return conta.id_conta
