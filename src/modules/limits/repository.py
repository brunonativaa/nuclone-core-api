from typing import Optional
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from src.modules.limits.models import LimiteContaModel


class LimitsRepository:
    def __init__(self, db: Session):
        self.db =db

    def get_by_conta(self, id_conta: int) -> Optional[LimiteContaModel]:
        stmt = select(LimiteContaModel).where(LimiteContaModel.id_conta == id_conta)
        return self.db.scalars(stmt).first()

    def update_limits(self, limite_obj: LimiteContaModel) -> LimiteContaModel:
        self.db.add(limite_obj)
        self.db.commit()
        self.db.refresh(limite_obj)
        return limite_obj