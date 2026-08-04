import pytest
from src.services.cliente_service import ClienteService
from src.services.conta_service import (ContaService,
                                        ClienteNaoEncontradoException,
                                        ContaNaoEncontradaException)


def test_create_account_success(db_session, valid_customer_data):
    """ Testa a criação de uma conta bancária vinculada a um cliente existente.
       Garante que o número da conta foi gerado automaticamente."""

    customer_service = ClienteService(db_session)
    account_service = ContaService(db_session)

    customer = customer_service.create_customer(valid_customer_data)

    account_data = {"id_cliente": customer.id_cliente, "tipo_conta": "PF"}
    account = account_service.create_account(account_data)

    assert account.id_conta is not None
    assert account.id_cliente == customer.id_cliente
    assert account.num_conta is not None


def test_get_initial_balance_zero(db_session, valid_customer_data):
    """ Testa se o saldo inicial da conta recém-criada é exatamente 0.00."""

    customer_service = ClienteService(db_session)
    account_service = ContaService(db_session)

    customer = customer_service.create_customer(valid_customer_data)
    account = account_service.create_account(
        {"id_cliente": customer.id_cliente})

    balance_info = account_service.get_saldo(account.id_conta)

    assert balance_info is not None
    assert float(balance_info.saldo_disponivel) == 0.00


def test_create_account_for_non_existing_customer_should_fail(db_session):
    """
    Testa a validação de integridade: proíbe a criação de conta para ID de cliente inexistente. """

    account_service = ContaService(db_session)

    with pytest.raises(ClienteNaoEncontradoException):
        account_service.create_account({"id_cliente": 9999999})
