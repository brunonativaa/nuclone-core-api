from typing import Optional
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload
from src.modules.account.model import ContaModel, SaldoContaModel


class ContaRepository:

    def __init__(self, db: Session):
        self.db = db

    def create_account(self, data) -> ContaModel:
        payload = data.model_dump() if isinstance(data, BaseModel) else data
        conta = ContaModel(**payload)
        self.db.add(conta)
        self.db.flush()
        self.db.refresh(conta)
        return conta

    def create_saldo(self, id_conta: int) -> SaldoContaModel:
        saldo = SaldoContaModel(id_conta=id_conta, saldo_disponivel=0.00)
        self.db.add(saldo)
        self.db.flush()
        return saldo

    def get_saldo(self, id_conta: int) -> Optional[SaldoContaModel]:
        stmt = ( 
            select(ContaModel)
            .options(joinedload(ContaModel.saldo))
            .where(ContaModel.id_conta == id_conta)
        )   
        conta = self.db.scalar(stmt)
        return conta.saldo if conta else None

    def search_account(self, id_conta: int) -> Optional[ContaModel]:

        return self.db.get(ContaModel, id_conta)