from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.customer.model import ClienteModel
from src.modules.account.model import ContaModel


class AuthRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_cliente_by_cpf(self, cpf: str) -> Optional[ClienteModel]:
        stmt = select(ClienteModel).where(ClienteModel.cpf == cpf)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_account_by_cliente_id(self, id_cliente: int) -> Optional[ContaModel]:
        stmt = select(ContaModel).where(ContaModel.id_cliente == id_cliente)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
