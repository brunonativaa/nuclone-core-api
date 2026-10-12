import random
from datetime import date
from decimal import Decimal
import pytest

from src.modules.account.repository import ContaRepository
from src.modules.account.service import ContaService
from src.modules.customer.repository import ClienteRepository
from src.modules.pix.service import PixService
from src.modules.account.exceptions import ContaNaoEncontradaException
from src.modules.pix.exceptions import SaldoInsuficienteException


@pytest.fixture
async def setup_two_accounts_with_balance(db_session, valid_customer_data):
    cliente_repo = ClienteRepository(db_session)
    account_service = ContaService(db_session)

    # 1. Cria Cliente Origem utilizando o ClienteRepository
    customer1 = await cliente_repo.create(valid_customer_data)

    # 2. Cria Conta Origem vinculada ao cliente 1
    source_account = await account_service.create_account(
        id_cliente=customer1.id_cliente,
        agencia="0001",
        tipo_conta="PF"
    )

    # Credita saldo inicial de R$ 100,00 na conta de origem
    await account_service.credit(source_account.id_conta, Decimal("100.00"))

    # 3. Cria Cliente Destino
    random_id = random.randint(1000, 9999)
    random_cpf = f"{random.randint(100, 999)}.{random.randint(100, 999)}.{random.randint(100, 999)}-00"

    customer2_data = {
        "nome": "Bruno Receiver Teste",
        "cpf": random_cpf,
        "sexo": "M",
        "email": f"receiver_{random_id}@email.com",
        "senha_hash": "secure_password_test",
        "pin_transacao_hash": "123456",
        "data_nascimento": date(1990, 1, 1),
    }
    customer2 = await cliente_repo.create(customer2_data)

    # 4. Cria Conta Destino para o segundo cliente
    destination_account = await account_service.create_account(
        id_cliente=customer2.id_cliente,
        agencia="0001",
        tipo_conta="PF"
    )

    await db_session.flush()

    return source_account, destination_account


@pytest.mark.asyncio
async def test_execute_pix_transaction_success(db_session, setup_two_accounts_with_balance):
    source_account, destination_account = setup_two_accounts_with_balance
    pix_service = PixService(db_session)
    account_service = ContaService(db_session)

    # Executa transferência PIX de R$ 40,00
    await pix_service.make_pix_payment(
        id_conta_origem=source_account.id_conta,
        id_conta_destino=destination_account.id_conta,
        valor=Decimal("40.00")
    )

    # Saldo final esperado: Origem (100 - 40 = 60), Destino (0 + 40 = 40)
    source_balance = await account_service.get_balance(source_account.id_conta)
    dest_balance = await account_service.get_balance(destination_account.id_conta)

    assert source_balance.saldo_disponivel == Decimal("60.00")
    assert dest_balance.saldo_disponivel == Decimal("40.00")


@pytest.mark.asyncio
async def test_execute_pix_insufficient_balance_should_fail(db_session, setup_two_accounts_with_balance):
    source_account, destination_account = setup_two_accounts_with_balance
    pix_service = PixService(db_session)

    with pytest.raises(SaldoInsuficienteException):
        await pix_service.make_pix_payment(
            id_conta_origem=source_account.id_conta,
            id_conta_destino=destination_account.id_conta,
            valor=Decimal("500.00")
        )


@pytest.mark.asyncio
async def test_execute_pix_invalid_destination_account_should_fail(db_session, setup_two_accounts_with_balance):
    source_account, _ = setup_two_accounts_with_balance
    pix_service = PixService(db_session)

    with pytest.raises(ContaNaoEncontradaException):
        await pix_service.make_pix_payment(
            id_conta_origem=source_account.id_conta,
            id_conta_destino=999999,
            valor=Decimal("10.00")
        )