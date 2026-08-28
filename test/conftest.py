import datetime
import random
import pytest
from fastapi.testclient import TestClient

from src.main import app
from src.core.database import engine, SessionLocal, get_db
from src.modules.account.account_model import ContaModel, SaldoContaModel
from src.modules.customer.customer_model import ClienteModel


@pytest.fixture(scope="function")
def db_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.rollback()  # Desfaz as alterações após cada teste
        session.close()


@pytest.fixture
def client(db_session):
    def _override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = _override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def valid_customer_data():
    random_number = random.randint(10000, 99999)
    # Gerador simples para evitar violação de UNIQUE constraint no CPF
    random_cpf = f"{random_number:05d}{random.randint(10000, 99999):05d}1"

    return {
        "nome": "Bruno Typer2@26",
        "cpf": random_cpf,
        "email": f"pytest_{random_number}@email.com",
        "senha": "senha_segura_test",
        "sexo": "M",
        "data_nascimento": "1997-08-15"
    }


@pytest.fixture
def id_conta_origem(db_session, valid_customer_data):
    cliente = ClienteModel(**valid_customer_data)
    db_session.add(cliente)
    db_session.flush()

    random_num = random.randint(10000, 99999)
    conta = ContaModel(
        id_cliente=cliente.id_cliente,
        num_conta=f"000{random_num}-1",
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
    db_session.commit()  # Garante persistência visível na API durante o teste

    return conta.id_conta


@pytest.fixture
def id_conta_destino(db_session):
    random_number = random.randint(10000, 99999)
    random_cpf = f"{random_number:05d}{random.randint(10000, 99999):05d}2"

    dados_destino = {
        "nome": "Cliente Destino Teste",
        "cpf": random_cpf,
        "email": f"destino_{random_number}@email.com",
        "senha": "senha_segura_test",
        "sexo": "F",
        "data_nascimento": "1998-01-01"
    }
    cliente = ClienteModel(**dados_destino)
    db_session.add(cliente)
    db_session.flush()

    conta = ContaModel(
        id_cliente=cliente.id_cliente,
        num_conta=f"000{random_number}-2",
        agencia="0001",
        tipo_conta="PF"
    )
    db_session.add(conta)
    db_session.flush()

    # 3. Cria o Saldo zerado
    saldo = SaldoContaModel(
        id_conta=conta.id_conta,
        saldo_disponivel=0,
        saldo_bloqueado=0,
        ultima_atualizacao=datetime.datetime.now(datetime.timezone.utc)
    )
    db_session.add(saldo)
    db_session.commit()  # Garante persistência visível na API durante o teste

    return conta.id_conta
