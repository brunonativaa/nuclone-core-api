from datetime import datetime
from typing import Optional
from decimal import Decimal
from src.modules.ledger.model import TipoTransacaoEnum, StatusTransacaoEnum
from pydantic import BaseModel, Field, ConfigDict


class ExtratoItemSchema(BaseModel):
    id_transacao: int
    id_conta_origem: int
    id_conta_destino: int
    tipo_transacao: TipoTransacaoEnum = Field(
        ..., description="Tipo do lançamento contábil")
    valor: Decimal = Field(..., description="Valor monetário da transação")
    status: StatusTransacaoEnum = Field(...,
                                        description="Status atual do registro no Ledger")
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True  # Serializa os Enums como strings no JSON de resposta
    )


class ResumoContaSchema(BaseModel):
    id_conta: int
    numero_conta: str
    agencia: str
    saldo: Decimal
    limite_credito: Decimal

    model_config = ConfigDict(from_attributes=True)


class ExtratoCompletoSchema(BaseModel):
    conta: ResumoContaSchema
    transacoes: list[ExtratoItemSchema]
