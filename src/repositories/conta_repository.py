from sqlalchemy.orm import Session
from src.models.conta_model import ContaModel
from src.models.saldo_conta_model import SaldoContaModel


class ContaRepository:

    def __init__(self, db: Session):
        self.db = db

    def create_account(self, data):
        conta = ContaModel(
            id_cliente=data["id_cliente"],
            num_conta=data["num_conta"],     # ✔ nome correto
            tipo_conta=data.get("tipo_conta", "PF"),
            agencia=data["agencia"]
        )
        self.db.add(conta)
        self.db.commit()
        self.db.refresh(conta)
        return conta

    def get_saldo(self, id_conta):
        return self.db.query(SaldoContaModel).filter_by(id_conta=id_conta).first()

    def create(self, data):
        return self.criar_conta(data)

    def search_account(self, id_conta):
        return self.db.query(ContaModel).filter_by(id_conta=id_conta).first()

    def create_saldo(self, id_conta):
        saldo = SaldoContaModel(id_conta=id_conta, saldo_disponivel=0)
        self.db.add(saldo)
        self.db.commit()
        return saldo
