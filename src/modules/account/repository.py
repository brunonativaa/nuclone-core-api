from typing import Optional
from decimal import Decimal
from pydantic import BaseModel
from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession 
from src.modules.account.model import ContaModel, SaldoContaModel


class ContaRepository:

    def __init__(self, db_session: AsyncSession):
        self.db = db_session

    async def create_account(self, id_cliente: int, agencia: str, num_conta: str, tipo_conta: str = "PF", id_conta: Optional[int] = None) -> ContaModel:
        account_data = {
            "id_cliente": id_cliente,
            "agencia": agencia,
            "num_conta": num_conta,
            "tipo_conta": tipo_conta
    }
    
        # Se o ID foi passado explicitamente (ex: nos testes com SQLite), injeta no dicionário
        if id_conta is not None:
            account_data["id_conta"] = id_conta

        conta = ContaModel(**account_data)
        self.db.add(conta)
        await self.db.flush()
        await self.db.refresh(conta)
        return conta

    async def create_balance(self, id_conta: int, saldo_inicial: Decimal = Decimal("0.00"), id_saldo_conta: Optional[int] = None) -> SaldoContaModel:
        balance_data = {
            "id_conta": id_conta,
            "saldo_disponivel": saldo_inicial,
            "saldo_bloqueado": Decimal("0.00"),
        }
    
        # Se o ID foi passado explicitamente (para satisfazer o SQLite nos testes), injeta no dicionário
        if id_saldo_conta is not None:
            balance_data["id_saldo_conta"] = id_saldo_conta

        saldo = SaldoContaModel(**balance_data)
        self.db.add(saldo)
        await self.db.flush()
        await self.db.refresh(saldo)
        return saldo

    async def get_account_by_id(self, id_conta: int) -> Optional[ContaModel]:
        return await self.db.get(ContaModel, id_conta)

    async def get_account_by_customer_id(self, id_cliente: int) -> Optional[ContaModel]:
        stmt = select(ContaModel).where(ContaModel.id_cliente == id_cliente)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def get_balance(self, id_conta: int) -> Optional[SaldoContaModel]:
        stmt = select(SaldoContaModel).where(SaldoContaModel.id_conta == id_conta)     
        return await self.db.scalar(stmt)

    async def get_balance_for_update(self, id_conta: int) -> Optional[SaldoContaModel]:
        """Aplica Pessimistic Locking (SELECT ... FOR UPDATE no PostgreSQL)."""
        stmt = (
            select(SaldoContaModel)
            .where(SaldoContaModel.id_conta == id_conta)
            .with_for_update()
        )
        return await self.db.scalar(stmt)

    async def update_balance_value(self, saldo_model: SaldoContaModel, novo_valor: Decimal) -> SaldoContaModel:
        """Apenas atualiza o modelo de saldo na sessão."""
        saldo_model.saldo_disponivel = novo_valor
        self.db.add(saldo_model)
        await self.db.flush()
        return saldo_model