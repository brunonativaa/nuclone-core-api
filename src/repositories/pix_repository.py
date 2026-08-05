from decimal import Decimal
from sqlalchemy.orm import Session
from src.models.transaction_model import TransacaoModel
from src.models.balance_account_model import SaldoContaModel


class PixRepository:

    def __init__(self, db: Session):
        self.db = db

    def update_saldo(self, id_conta, valor):
        saldo = self.db.query(SaldoContaModel).filter_by(
            id_conta=id_conta).first()
        saldo.saldo_disponivel += Decimal(str(valor))
        self.db.commit()
        return saldo

    def debitar(self, id_conta, valor):
        # Passa o valor negativo para subtrair
        return self.update_saldo(id_conta, -Decimal(str(valor)))

    def creditar(self, id_conta, valor):
        # Passa o valor positivo para somar
        return self.update_saldo(id_conta, Decimal(str(valor)))

    def record_transaction(self, data: dict):
        transacao = TransacaoModel(**data)
        self.db.add(transacao)
        self.db.commit()
        self.db.refresh(transacao)
        return transacao
