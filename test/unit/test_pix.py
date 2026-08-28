import random
from decimal import Decimal
import pytest
from src.modules.customer.customer_service import ClienteService
from src.modules.account.account_service import ContaService
from src.modules.pix.pix_service import (
    PixService,
    SaldoInsuficienteException,
    ContaNaoEncontradaException
)


@pytest.fixture
def setup_two_accounts_with_balance(db_session, valid_customer_data):
    """
    Fixture de preparação: cria 2 clientes, 2 contas e injeta R$ 100,00 de saldo
    na conta de origem para viabilizar as simulações de PIX.
    """
    customer_service = ClienteService(db_session)
    account_service = ContaService(db_session)

    # Origem (Sender)
    customer1 = customer_service.create_customer(valid_customer_data)
    source_account = account_service.create_account(
        {"id_cliente": customer1.id_cliente})

    # Busca o registro de saldo e atualiza para R$ 100,00
    source_balance = account_service.get_saldo(source_account.id_conta)
    source_balance.saldo_disponivel = Decimal("100.00")
    db_session.add(source_balance)

    random_id = random.randint(100000, 999999)
    random_cpf = f"{random.randint(100, 999)}.{random.randint(100, 999)}.{random.randint(100, 999)}-00"
    customer2_data = {
        "nome": f"Bruno Typer2026",
        "cpf": random_cpf,  # Exatamente 11 dígitos
        "email": f"receiver_{random_id}@email.com",
        "senha": "secure_password_test",
        "sexo": "F",
        "data_nascimento": "1995-05-20"
    }
    customer2 = customer_service.create_customer(customer2_data)
    destination_account = account_service.create_account(
        {"id_cliente": customer2.id_cliente})

    # Sincroniza a alteração de saldo e a criação da segunda conta na sessão do teste
    db_session.flush()

    return source_account, destination_account


def test_execute_pix_transaction_success(db_session, setup_two_accounts_with_balance):
    """
Testa o fluxo completo de uma transação PIX com sucesso.
Verifica o débito na conta de origem (100 - 40 = 60) e o crédito na conta de destino (0 + 40 = 40). """

    source_account, destination_account = setup_two_accounts_with_balance
    pix_service = PixService(db_session)
    account_service = ContaService(db_session)

    # Executa transferência PIX de R$ 40,00
    pix_service.realizar_pix(
        id_conta_origem=source_account.id_conta,
        id_conta_destino=destination_account.id_conta,
        valor=Decimal("40.00")
    )

    # Consulta os saldos pós-transação
    updated_source_balance = account_service.get_saldo(
        source_account.id_conta).saldo_disponivel
    updated_destination_balance = account_service.get_saldo(
        destination_account.id_conta).saldo_disponivel

    assert float(updated_source_balance) == 60.00
    assert float(updated_destination_balance) == 40.00


def test_execute_pix_insufficient_balance_should_fail(db_session, setup_two_accounts_with_balance):
    """Testa a regra de proteção financeira: impede transferência quando o valor excede o saldo disponível."""
    source_account, destination_account = setup_two_accounts_with_balance
    pix_service = PixService(db_session)

    # Tenta enviar R$ 500,00 possuindo apenas R$ 100,00 em conta
    with pytest.raises(SaldoInsuficienteException):
        pix_service.realizar_pix(
            id_conta_origem=source_account.id_conta,
            id_conta_destino=destination_account.id_conta,
            valor=Decimal("500.00")
        )


def test_execute_pix_invalid_destination_account_should_fail(db_session, setup_two_accounts_with_balance):
    """ Testa a tentativa de transferência para uma conta de destino que não existe no banco de dados."""
    source_account, _ = setup_two_accounts_with_balance
    pix_service = PixService(db_session)

    with pytest.raises(ContaNaoEncontradaException):
        pix_service.realizar_pix(
            id_conta_origem=source_account.id_conta,
            id_conta_destino=999999,
            valor=Decimal("10.00")
        )
