from sqlalchemy.orm import Session
from src.models.account_model import ContaModel
from src.models.balance_account_model import SaldoContaModel


class ContaRepository:

    def __init__(self, db: Session):
        self.db = db

    def create_account(self, data: dict) -> ContaModel:
        conta = ContaModel(
            id_cliente=data["id_cliente"],
            num_conta=data["num_conta"],
            tipo_conta=data.get("tipo_conta", "PF"),
            agencia=data.get("agencia", "0001")
        )
        self.db.add(conta)
        self.db.flush()  # Envia pro banco e gera o id_conta sem fechar a transação
        self.db.refresh(conta)
        return conta

    def create_saldo(self, id_conta: int) -> SaldoContaModel:
        saldo = SaldoContaModel(id_conta=id_conta, saldo_disponivel=0)
        self.db.add(saldo)
        self.db.flush()
        return saldo

    def get_saldo(self, id_conta: int) -> SaldoContaModel | None:
        return self.db.query(SaldoContaModel).filter_by(id_conta=id_conta).first()

    def search_account(self, id_conta: int) -> ContaModel | None:
        return self.db.query(ContaModel).filter_by(id_conta=id_conta).first()
