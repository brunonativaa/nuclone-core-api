import pytest
from pydantic import ValidationError
from src.modules.customer.service import (
    ClienteService,
    ClienteJaExisteException,
    ClienteNaoEncontradoException
)
from src.modules.customer.schema import ClienteCreateInput


def test_create_customer_siccess_with_dict(db_session, valid_customer_data):

    # 1. Arrange
    service = ClienteService(db_session)
    data = valid_customer_data.copy()
    data["cpf"] = "123.456.789-00" # tst higienização do CPF (Rows 31 - 33)

    # 2. Act
    cliente_criado = service.create_customer(data)

    # 3. Assert
    assert cliente_criado.id_cliente is not None
    assert cliente_criado.cpf == "12345678900" # CPF sem pontos/traços
    assert cliente_criado.senha_hash != "senha123" # Deve ter sido criptografada (row 54)

def test_create_customer_success_with_dto(db_session, valid_customer_data):
    """Testa o suporte a envio de DTO diretamente (rows 24-25 do código)."""

    service = ClienteService(db_session)
    dto = ClienteCreateInput(**valid_customer_data)

    cliente_criado = service.create_customer(dto)

    assert cliente_criado.id_cliente is not None
    assert cliente_criado.email == valid_customer_data["email"]

def test_get_customer_by_id_success(db_session, valid_customer_data):
    """Testa a busca de cliente existente por ID (rows 67-71)."""
    
    service = ClienteService(db_session)
    criado = service.create_customer(valid_customer_data)

    encontrado = service.get_by_id(criado.id_cliente)

    assert encontrado.id_cliente == criado.id_cliente
    assert encontrado.email == criado.email

def test_get_all_customers_returns_list(db_session, valid_customer_data):

    """Testa a listagem de todos os clientes (rows 72-74)."""
    service = ClienteService(db_session)
    service.create_customer(valid_customer_data)

    lista = service.get_all()

    assert len(lista) > 0


def test_create_customer_duplicate_cpf_should_fail(db_session, valid_customer_data):
    """Testa a regra de negócio que impede o cadastro de CPFs duplicados."""

    service = ClienteService(db_session)
    service.create_customer(valid_customer_data)

    duplicate_data = valid_customer_data.copy()
    duplicate_data["email"] = "other_email@email.com"

    with pytest.raises(ClienteJaExisteException) as exc_info:
        service.create_customer(duplicate_data)

    assert "Já existe um cliente cadastrado com esse CPF." in str(exc_info.value)

def test_create_customer_missing_password_or_pin_should_fail(db_session, valid_customer_data):
    """Testa a validação de ausência de senha/PIN (linhas 49-51)."""

    service = ClienteService(db_session)

    data_sem_senha = valid_customer_data.copy()
    data_sem_senha.pop("senha_hash", None)
    data_sem_senha.pop("senha", None)

    with pytest.raises(ValidationError) as exc_info:
        service.create_customer(data_sem_senha)

    assert "senha_hash" in str(exc_info.value)
    assert "Field required" in str(exc_info.value) 


def test_get_customer_by_non_existing_id_should_fail(db_session):

    """Testa o tratamento ao buscar ID inexistente (linhas 68-70)."""
    service = ClienteService(db_session)

    with pytest.raises(ClienteNaoEncontradoException) as exc_info:
        service.get_by_id(id_cliente=999999)

    assert "Cliente não encontrado" in str(exc_info.value)


def test_create_customer_rollback_on_database_erro(db_session, valid_customer_data, monkeypatch):
    """Testa o bloco 'except Exception' com rollback (linhas 62-64) usando 
       monkepatch para simular uma falha forçada"""

    service = ClienteService(db_session)

    def mock_create_error(*args, **kwargs):
        raise RuntimeError("Erro génerico no banco de dados")

    monkeypatch.setattr(service.customer_repo, "create", mock_create_error)

    with pytest.raises(RuntimeError):
        service.create_customer(valid_customer_data)