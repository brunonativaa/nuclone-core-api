import random
import pytest
from sqlalchemy.orm import sessionmaker
from src.core.database import Base, engine, SessionLocal
from src.models.account_model import ContaModel
from src.models.balance_account_model import SaldoContaModel
# Importe a sua model de Cliente (ajuste o caminho de import se for diferente)
from src.models.customer_model import ClienteModel


@pytest.fixture(scope="function")
def db_session():
    connection = engine.connect()
    transaction = connection.begin()

    session = SessionLocal(
        bind=connection, join_transaction_mode="create_savepoint"
    )

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def valid_customer_data():
    random_number = random.randint(10000, 99999)

    return {
        "nome": "Bruno Typer2@26",
        "cpf": f"{random_number}877701",
        "email": f"pytest_{random_number}@email.com",
        "senha": "senha_segura_test",
        "sexo": "M",
        "data_nascimento": "1997-08-15"
    }


@pytest.fixture
def id_conta_origem(db_session, valid_customer_data):
    # 1. Cria o Cliente primeiro para satisfazer a ForeignKey
    cliente = ClienteModel(**valid_customer_data)
    db_session.add(cliente)
    db_session.flush()

    # 2. Cria a Conta passando id_cliente, num_conta e agencia
    random_num = random.randint(10000, 99999)
    conta = ContaModel(
        id_cliente=cliente.id_cliente,  # Ajuste para cliente.id se o atributo for .id
        num_conta=f"000{random_num}-1",
        agencia="0001",
        tipo_conta="PF"
    )
    db_session.add(conta)
    db_session.flush()

    # 3. Cria o Saldo zerado vinculado à conta (usando conta.id_conta)
    saldo = SaldoContaModel(id_conta=conta.id_conta, saldo_disponivel=0)
    db_session.add(saldo)
    db_session.flush()

    return conta.id_conta


@pytest.fixture
def id_conta_destino(db_session):
    # 1. Cria o segundo Cliente
    random_number = random.randint(10000, 99999)
    dados_destino = {
        "nome": "Cliente Destino Teste",
        "cpf": f"{random_number}123456",
        "email": f"destino_{random_number}@email.com",
        "senha": "senha_segura_test",
        "sexo": "F",
        "data_nascimento": "1998-01-01"
    }
    cliente = ClienteModel(**dados_destino)
    db_session.add(cliente)
    db_session.flush()

    # 2. Cria a Conta de destino
    conta = ContaModel(
        id_cliente=cliente.id_cliente,
        num_conta=f"000{random_number}-2",
        agencia="0001",
        tipo_conta="PF"
    )
    db_session.add(conta)
    db_session.flush()

    # 3. Cria o Saldo zerado
    saldo = SaldoContaModel(id_conta=conta.id_conta, saldo_disponivel=0)
    db_session.add(saldo)
    db_session.flush()

    return conta.id_conta
