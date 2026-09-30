from datetime import datetime, timedelta, timezone
from decimal import Decimal
from src.modules.ledger.repository import LedgerRepository
from src.modules.ledger.model import TransacaoModel, StatusTransacaoEnum, TipoTransacaoEnum

def test_ledger_repository_get_by_id_and_extrato(db_session):
    repo = LedgerRepository(db_session)
    agora = datetime.utcnow()

    assert repo.get_by_id(id_transacao=99999) is None

    t1 = TransacaoModel(
        id_conta_origem=1,
        id_conta_destino=2,
        tipo_transacao=TipoTransacaoEnum.PIX,
        valor=Decimal("150.00"),
        status=StatusTransacaoEnum.CONCLUIDO,
        is_noturno=False,
        created_at=agora - timedelta(days=2)
    )
    t2 = TransacaoModel(
        id_conta_origem=2,
        id_conta_destino=1,
        tipo_transacao=TipoTransacaoEnum.PIX,
        valor=Decimal("50.00"),
        status=StatusTransacaoEnum.CONCLUIDO,
        is_noturno=True,
        created_at=agora - timedelta(days=1)
    )

    db_session.add_all([t1, t2])
    db_session.commit()

    transacao_db = repo.get_by_id(t1.id_transacao)
    assert transacao_db is not None
    assert transacao_db.valor == Decimal("150.00")

    data_inicio = agora - timedelta(days=3)
    data_fim = agora 

    extrato = repo.get_extrato_by_conta(
        id_conta=1,
        limit=10,
        offset=0,
        data_inicio=data_inicio,
        data_fim=data_fim
    )
    assert len(extrato) == 2

def test_ledger_repository_get_total_gasto_janela(db_session):
    repo = LedgerRepository(db_session)
    agora = datetime.now(timezone.utc)
    inicio = agora - timedelta(hours=1)
    fim = agora + timedelta(hours=1)


    t_concluida = TransacaoModel(
        id_conta_origem =10,
        id_conta_destino =20,
        tipo_transacao=TipoTransacaoEnum.PIX,
        valor=Decimal("200.00"),
        status=StatusTransacaoEnum.CONCLUIDO,
        is_noturno=False,
        created_at=agora  
    )

    # Transação noturna (não deve somar no cálculo diurno)
    t_noturna = TransacaoModel(
        id_conta_origem=10,
        id_conta_destino=20,
        tipo_transacao=TipoTransacaoEnum.PIX,
        valor=Decimal("500.00"),
        status=StatusTransacaoEnum.CONCLUIDO,
        is_noturno=True,
        created_at=agora
    )

    db_session.add_all([t_concluida, t_noturna])
    db_session.commit()

    # Total gasto diurno na janela
    total_diurno = repo.get_total_gasto_janela(
        id_conta=10,
        inicio=inicio,
        fim=fim,
        is_noturno=False
    )
    assert total_diurno == Decimal("200.00")

    # Total gasto em conta sem transações (deve retornar Decimal 0)
    total_vazio = repo.get_total_gasto_janela(
        id_conta=999,
        inicio=inicio,
        fim=fim,
        is_noturno=False
    )
    assert total_vazio == Decimal("0")