import pytest
from src.modules.account.schema import AccountCreateInput
from src.modules.account.service import (
    ClienteNaoEncontradoException,
    ContaService,
)
from src.modules.customer.schema import ClienteCreateInput
from src.modules.customer.service import ClienteService


async def _ensure_customer_input(data) -> ClienteCreateInput:
    """Helper interno para garantir a conversão do payload em DTO válido."""
    return data if isinstance(data, ClienteCreateInput) else ClienteCreateInput(**data)


async def test_create_account_success(db_session, valid_customer_data):
    """Testa a criação de uma conta bancária vinculada a um cliente existente."""
    customer_service = ClienteService(db_session)
    account_service = ContaService(db_session)

    customer_input = await _ensure_customer_input(valid_customer_data)
    customer = await customer_service.create_customer(customer_input)

    account_data = AccountCreateInput(
        id_cliente=customer.id_cliente, tipo_conta="PF"
    )
   
    account = await account_service.create_account(
        id_cliente=account_data.id_cliente,
        agencia=account_data.agencia,
        tipo_conta=account_data.tipo_conta,
    )

    assert account.id_conta is not None
    assert account.id_cliente == customer.id_cliente
    assert account.num_conta is not None


async def test_get_initial_balance_zero(db_session, valid_customer_data):
    """Testa se o saldo inicial da conta recém-criada é exatamente 0.00."""
    customer_service = ClienteService(db_session)
    account_service = ContaService(db_session)

    customer_input = await _ensure_customer_input(valid_customer_data)
    customer = await customer_service.create_customer(customer_input)

    account_input = AccountCreateInput(
        id_cliente=customer.id_cliente, tipo_conta="PF"
    )
    account = await account_service.create_account(
        id_cliente=account_input.id_cliente,
        agencia=account_input.agencia,
        tipo_conta=account_input.tipo_conta,
    )

    balance_info = await account_service.get_balance(account.id_conta)

    assert balance_info is not None
    assert float(balance_info.saldo_disponivel) == 0.00


async def test_create_account_for_non_existing_customer_should_fail(db_session):
    """Garante falha ao tentar criar conta para cliente inexistente."""
    account_service = ContaService(db_session)
    invalid_account_input = AccountCreateInput(id_cliente=9999999)

    with pytest.raises(ClienteNaoEncontradoException):
        # ✅ Passa o id_cliente como int
        await account_service.create_account(
            id_cliente=invalid_account_input.id_cliente,
            agencia=invalid_account_input.agencia,
            tipo_conta=invalid_account_input.tipo_conta,
        )