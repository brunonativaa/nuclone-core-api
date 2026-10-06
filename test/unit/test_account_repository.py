import pytest
from src.modules.account.repository import ContaRepository
from src.modules.account.service import ContaService
from src.modules.account.model import ContaModel, SaldoContaModel


async def test_get_balance_creates_opening_balance_when_none_exists(db_session):
    repo = ContaRepository(db_session)
    service = ContaService(db_session)
    # 1. Cria uma conta no banco 
    new_account = ContaModel(
        id_cliente=1,
        num_conta="1254585",
        tipo_conta="PJ",
        agencia="0001"
    )

    db_session.add(new_account)
    await db_session.commit()
    await db_session.refresh(new_account)

    # 2. Chama get_saldo para a conta recém-criada
    saldo = await service.get_balance(id_conta=new_account.id_conta)

    assert saldo is not None
    assert saldo.saldo_disponivel == 0.00
    assert saldo.saldo_bloqueado == 0.00
    assert saldo.id_conta == new_account.id_conta