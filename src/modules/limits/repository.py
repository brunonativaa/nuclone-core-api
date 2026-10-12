from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.limits.model import LimiteContaModel


class LimitesRepository:
    def __init__(self, db: AsyncSession):
        self.db =db

    async def get_by_conta(self, id_conta: int, for_update: bool = False) -> Optional[LimiteContaModel]:
        stmt = select(LimiteContaModel).where(LimiteContaModel.id_conta == id_conta)
        if for_update:
            stmt = stmt.with_for_update()
        result = await self.db.scalars(stmt)
        return result.first()

    async def update_limits(self, limite_obj: LimiteContaModel) -> LimiteContaModel:
       
        self.db.add(limite_obj)
        await self.db.commit()
        await self.db.refresh(limite_obj)
        return limite_obj