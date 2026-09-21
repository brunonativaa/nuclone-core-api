from datetime import datetime
from typing import Optional
from decimal import Decimal
from src.modules.ledger.models import TipoTransacaoEnum
from pydantic import BaseModel, Field

class TransactionResponseSchema(BaseModel):
    """Payload de resposta para transações"""
    id_transacao: int
    id_conta_origem: int
    id_conta_destino: int
    tipo_transacao: TipoTransacaoEnum
    valor: Decimal = Field(..., gt=0, description="Valor da transação")
    status: TipoTransacaoEnum
    created_at: datetime

class ExtratoQuerySchema(BaseModel):
    data_inicio: Optional[datetime] = None
    data_fim: Optional[datetime] = None
    limit: int = Field(defaut=20, ge=1, le=100)
    offset: int = Field(default=0, ge=0)

    