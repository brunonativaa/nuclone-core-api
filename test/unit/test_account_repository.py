import pytest
import random
from datetime import date
from src.modules.account.repository import ContaRepository
from src.modules.account.service import ContaService
from src.modules.account.model import ContaModel, SaldoContaModel
from src.modules.customer.model import ClienteModel 


@pytest.mark.asyncio
async def test_get_balance_creates_opening_balance_when_none_exists(db_session):
    repo = ContaRepository(db_session)
    service = ContaService(db_session)
    
    id_cliente_teste = random.randint(10000, 999999)
    id_conta_teste = random.randint(10000, 999999)

    # 1. Criação prévia do Cliente pai para satisfazer a FK da tabela contas
    cliente_pai = ClienteModel(
        id_cliente=id_cliente_teste,
        nome="Cliente Teste Account Repo",
        cpf="12345678903",
        email=f"cliente_{id_cliente_teste}@email.com",
        senha_hash="fake_hash",
        pin_transacao_hash="1234",
        sexo="M",
        data_nascimento=date(1990, 1, 1)
    )
    db_session.add(cliente_pai)
    await db_session.flush()

    # 2. Criação da conta vinculada ao cliente recém-criado
    new_account = ContaModel(
        id_conta=id_conta_teste,
        id_cliente=id_cliente_teste,
        num_conta="1254585",
        tipo_conta="PJ",
        agencia="0001"
    )

    db_session.add(new_account)
    await db_session.commit()
    await db_session.refresh(new_account)

    # 3. Chama get_saldo para a conta recém-criada
    saldo = await service.get_balance(id_conta=new_account.id_conta)

    assert saldo is not None
    assert saldo.saldo_disponivel == 0.00
    assert saldo.saldo_bloqueado == 0.00
    assert saldo.id_conta == new_account.id_conta