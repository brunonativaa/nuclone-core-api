from typing import Optional
from pydantic import BaseModel
from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession 
from src.modules.account.model import ContaModel, SaldoContaModel


class ContaRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_account(self, data) -> ContaModel:
        payload = data.model_dump() if isinstance(data, BaseModel) else data
        conta = ContaModel(**payload)
        self.db.add(conta)
        await self.db.flush()
        await self.db.refresh(conta)
        return conta

    async def create_balance(self, id_conta: int) -> SaldoContaModel:
        saldo = SaldoContaModel(id_conta=id_conta, saldo_disponivel=0.00)
        self.db.add(saldo)
        await self.db.flush()
        return saldo

    async def get_balance(self, id_conta: int) -> Optional[SaldoContaModel]:
        stmt = select(SaldoContaModel).where(SaldoContaModel.id_conta == id_conta)
        result = await self.db.execute(stmt)
        saldo =  result.scalar_one_or_none()
        
        return saldo
    
    async def search_account(self, id_conta: int) -> Optional[ContaModel]:

        return await self.db.get(ContaModel, id_conta)