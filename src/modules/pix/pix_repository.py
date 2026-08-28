from decimal import Decimal
from typing import Optional
from sqlalchemy import or_
from sqlalchemy.orm import Session
from src.modules.account.account_model import ContaModel, TransacaoModel, SaldoContaModel
from src.modules.customer.customer_model import ClienteModel, TelefoneModel


class PixRepository:

    def __init__(self, db: Session):
        self.db = db

    def search_account_by_key(self, key: str) -> Optional[ContaModel]:
        return (
            self.db.query(ContaModel)
            .join(ClienteModel, ContaModel.id_cliente == ClienteModel.id_cliente)
            .outerjoin(TelefoneModel, ClienteModel.id_cliente == TelefoneModel.id_cliente)
            .filter(
                or_(
                    ClienteModel.cpf == key,
                    ClienteModel.email == key,
                    TelefoneModel.numero == key
                )
            )
            .first()
        )

    def update_saldo(self, id_conta, valor):
        saldo = self.db.query(SaldoContaModel).filter_by(
            id_conta=id_conta).first()

        if not saldo:
            return None

        saldo.saldo_disponivel += Decimal(str(valor))

        self.db.add(saldo)
        return saldo

    def debit(self, id_conta, valor):
        # Passa o valor negativo para subtrair
        return self.update_saldo(id_conta, -Decimal(str(valor)))

    def credit(self, id_conta, valor):
        # Passa o valor positivo para somar
        return self.update_saldo(id_conta, Decimal(str(valor)))

    def record_transaction(self, data: dict):
        transacao = TransacaoModel(
            id_conta_origem=data["id_conta_origem"],
            id_conta_destino=data["id_conta_destino"],
            tipo_transacao=data["tipo_transacao"],
            valor=data["valor"]
        )
        self.db.add(transacao)
        self.db.flush()

        return transacao
