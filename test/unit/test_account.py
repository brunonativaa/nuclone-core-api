import pytest
from src.modules.account.schema import AccountCreateInput
from src.modules.account.service import (
    ClienteNaoEncontradoException,
    ContaService,
)
from src.modules.customer.schema import ClienteCreateInput
from src.modules.customer.service import ClienteService


def _ensure_customer_input(data) -> ClienteCreateInput:
    """Helper interno para garantir a conversão do payload em DTO válido."""
    return data if isinstance(data, ClienteCreateInput) else ClienteCreateInput(**data)


def test_create_account_success(db_session, valid_customer_data):
    """Testa a criação de uma conta bancária vinculada a um cliente existente."""
    customer_service = ClienteService(db_session)
    account_service = ContaService(db_session)

    customer_input = _ensure_customer_input(valid_customer_data)
    customer = customer_service.create_customer(customer_input)

    account_data = AccountCreateInput(
        id_cliente=customer.id_cliente, tipo_conta="PF"
    )
    account = account_service.create_account(account_data)

    assert account.id_conta is not None
    assert account.id_cliente == customer.id_cliente
    assert account.num_conta is not None


def test_get_initial_balance_zero(db_session, valid_customer_data):
    """Testa se o saldo inicial da conta recém-criada é exatamente 0.00."""
    customer_service = ClienteService(db_session)
    account_service = ContaService(db_session)

    customer_input = _ensure_customer_input(valid_customer_data)
    customer = customer_service.create_customer(customer_input)

    account_input = AccountCreateInput(
        id_cliente=customer.id_cliente, tipo_conta="PF"
    )
    account = account_service.create_account(account_input)

    balance_info = account_service.get_saldo(account.id_conta)

    assert balance_info is not None
    assert float(balance_info.saldo_disponivel) == 0.00


def test_create_account_for_non_existing_customer_should_fail(db_session):
    """Garante falha ao tentar criar conta para cliente inexistente."""
    account_service = ContaService(db_session)
    invalid_account_input = AccountCreateInput(id_cliente=9999999)

    with pytest.raises(ClienteNaoEncontradoException):
        account_service.create_account(invalid_account_input)
