import random
from datetime import datetime, timedelta, timezone, date
from decimal import Decimal
from src.modules.ledger.repository import LedgerRepository
from src.modules.ledger.model import TransacaoModel, StatusTransacaoEnum, TipoTransacaoEnum
from src.modules.account.model import ContaModel, TipoContaEnum
from src.modules.customer.model import ClienteModel  

async def test_ledger_repository_get_by_id_and_extrato(db_session):
    repo = LedgerRepository(db_session)
    agora = datetime.now(timezone.utc)

    assert await repo.get_by_id(id_transacao=99999) is None

    # 1. Criação prévia do Cliente pai para satisfazer a FK da tabela contas
    cliente_pai = ClienteModel(
        id_cliente=1,
        nome="Cliente Teste Ledger",
        cpf="12345678901",
        email="cliente_ledger@email.com",
        senha_hash="fake_hash",
        pin_transacao_hash="1234",
        sexo="M",
        data_nascimento=date(1990, 1, 1)
    )
    db_session.add(cliente_pai)
    await db_session.flush()

    # 2. Criação prévia das contas vinculadas ao cliente 1
    conta1 = ContaModel(id_conta=1, id_cliente=1, num_conta="00001-1", tipo_conta=TipoContaEnum.PF, agencia="0001")
    conta2 = ContaModel(id_conta=2, id_cliente=1, num_conta="00002-2", tipo_conta=TipoContaEnum.PF, agencia="0001")
    db_session.add_all([conta1, conta2])
    await db_session.flush()

    # 3. Criação das transações com IDs explícitos (mantendo o restante do teste...)
    t1 = TransacaoModel(
        id_transacao=random.randint(10000, 999999),
        id_conta_origem=1,
        id_conta_destino=2,
        tipo_transacao=TipoTransacaoEnum.PIX,
        valor=Decimal("150.00"),
        status=StatusTransacaoEnum.CONCLUIDO,
        is_noturno=False,
        created_at=agora - timedelta(days=2)
    )
    # ... Restante do código do teste