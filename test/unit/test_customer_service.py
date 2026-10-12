import pytest
from pydantic import ValidationError
from src.modules.customer.service import ClienteService
from src.modules.customer.repository import ClienteRepository
from src.modules.customer.schema import ClienteCreateInput
from src.modules.customer.exceptions import ClienteJaExisteException, ClienteNaoEncontradoException


async def test_create_customer_siccess_with_dict(db_session, valid_customer_data):

    # 1. Arrange
    service = ClienteService(db_session)
    data = valid_customer_data.copy()
    data["cpf"] = "123.456.789-00" # tst higienização do CPF (Rows 31 - 33)

    # 2. Act
    cliente_criado = await service.create_customer(data)

    # 3. Assert
    assert cliente_criado.id_cliente is not None
    assert cliente_criado.cpf == "12345678900" # CPF sem pontos/traços
    assert cliente_criado.senha_hash != "senha123" # Deve ter sido criptografada (row 54)

async def test_create_customer_success_with_dto(db_session, valid_customer_data):

    service = ClienteService(db_session)
    dto = ClienteCreateInput(**valid_customer_data)

    cliente_criado = await service.create_customer(dto)

    assert cliente_criado.id_cliente is not None
    assert cliente_criado.email == valid_customer_data["email"]

async def test_get_customer_by_id_success(db_session, valid_customer_data):
    
    service = ClienteService(db_session)
    criado = await service.create_customer(valid_customer_data)

    encontrado = await service.get_by_id(criado.id_cliente)

    assert encontrado.id_cliente == criado.id_cliente
    assert encontrado.email == criado.email

async def test_get_all_customers_returns_list(db_session, valid_customer_data):

    cliente_repo = ClienteRepository(db_session)
    cliente_service = ClienteService(db_session)

    await cliente_service.create_customer(valid_customer_data)

    lista = await cliente_repo.get_all()

    assert len(lista) > 0


async def test_create_customer_duplicate_cpf_should_fail(db_session, valid_customer_data):
    """Testa a regra de negócio que impede o cadastro de CPFs duplicados."""

    service = ClienteService(db_session)
    await service.create_customer(valid_customer_data)

    duplicate_data = valid_customer_data.copy()
    duplicate_data["email"] = "other_email@email.com"

    with pytest.raises(ClienteJaExisteException) as exc_info:
        await service.create_customer(duplicate_data)

    assert "Já existe um cliente cadastrado com esse CPF." in str(exc_info.value)

async def test_create_customer_missing_password_or_pin_should_fail(db_session, valid_customer_data):
    """Testa a validação de ausência de senha/PIN """
    service = ClienteService(db_session)

    data_sem_senha = valid_customer_data.copy()
    data_sem_senha.pop("senha_hash", None)
    data_sem_senha.pop("senha", None)

    with pytest.raises(ValueError, match="Senha e PIN de transação são obrigatórios") as exc_info:
        await service.create_customer(data_sem_senha)

    assert "Senha e PIN de transação são obrigatórios para o cadastro." in str(exc_info.value)


async def test_get_customer_by_non_existing_id_should_fail(db_session):
    customer_service = ClienteService(db_session)

    with pytest.raises(ClienteNaoEncontradoException) as exc_info:
        await customer_service.get_by_id(id_cliente=999999)

    assert "Cliente 999999 não encontrado" in str(exc_info.value)


async def test_create_customer_rollback_on_database_erro(db_session, valid_customer_data, monkeypatch):

    service = ClienteService(db_session)

    def mock_create_error(*args, **kwargs):
        raise RuntimeError("Erro génerico no banco de dados")

    monkeypatch.setattr(service.customer_repo, "create", mock_create_error)

    with pytest.raises(RuntimeError):
        await service.create_customer(valid_customer_data)