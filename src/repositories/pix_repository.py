from decimal import Decimal
from sqlalchemy.orm import Session
from src.models.transacao_model import TransacaoModel
from src.models.saldo_conta_model import SaldoContaModel


class PixRepository:

    def __init__(self, db: Session):
        self.db = db

    def atualizar_saldo(self, id_conta, valor):
        saldo = self.db.query(SaldoContaModel).filter_by(
            id_conta=id_conta).first()
        saldo.saldo_disponivel += Decimal(str(valor))
        self.db.commit()
        return saldo


    def registrar_transacao(self, data: dict):
        transacao = TransacaoModel(**data)
        self.db.add(transacao)
        self.db.commit()
        self.db.refresh(transacao)
        return transacao