from decimal import Decimal
from datetime import datetime
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_

from src.modules.ledger.model import TransacaoModel, StatusTransacaoEnum


class LedgerRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, id_transacao: int) -> Optional[TransacaoModel]:
        stmt = select(TransacaoModel).where(
            TransacaoModel.id_transacao == id_transacao
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_extrato_by_conta(
        self,
        id_conta: int,
        limit: int = 20,
        offset: int = 0,
        data_inicio: Optional[datetime] = None,
        data_fim: Optional[datetime] = None
    ) -> List[TransacaoModel]:

        stmt = select(TransacaoModel).where(
            or_(
                TransacaoModel.id_conta_origem == id_conta,
                TransacaoModel.id_conta_destino == id_conta
            )
        )

        if data_inicio:
            stmt = stmt.where(TransacaoModel.created_at >= data_inicio)
        if data_fim:
            stmt = stmt.where(TransacaoModel.created_at <= data_fim)

        stmt = stmt.order_by(TransacaoModel.created_at.desc()
                             ).limit(limit).offset(offset)

        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_total_gasto_janela(
        self,
        id_conta: int,
        inicio: datetime,
        fim: datetime
    ) -> Decimal:
        """
        Soma o total transacionado (saídas/débitos) dentro de uma janela de tempo específica.
        Utilizado para validação de limites diários e limites noturnos do Pix.
        """
        stmt = select(
            func.coalesce(func.sum(TransacaoModel.valor), Decimal("0.00"))
        ).where(
            TransacaoModel.id_conta_origem == id_conta,
            TransacaoModel.status == StatusTransacaoEnum.CONCLUIDO,
            TransacaoModel.created_at >= inicio,
            TransacaoModel.created_at <= fim
        )
        result = await self.db.execute(stmt)
        resultado = result.scalar()
        return Decimal(str(resultado)) if resultado is not None else Decimal("0.00")
