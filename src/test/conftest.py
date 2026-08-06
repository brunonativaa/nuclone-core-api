import random
import pytest
from src.core.database import engine, SessionLocal


@pytest.fixture(scope="function")
def db_session():

    connection = engine.connect()
    transaction = connection.begin()

    session = SessionLocal(
        bind=connection, join_transaction_mode="create_savepoint")

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def valid_customer_data():

    random_number = random.randint(10000, 99999)
    

    return {
        "nome": f"Bruno Typer2@26",
        "cpf": "99988877701",
        "email": f"pytest_{random_number}@email.com",
        "senha": "senha_segura_test",
        "sexo": "M",
        "data_nascimento": "1997-08-15"
    }
