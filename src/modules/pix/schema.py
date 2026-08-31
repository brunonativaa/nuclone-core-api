from pydantic import BaseModel, field_validator
from decimal import Decimal
from typing import Literal

# 1. Schema para Cadastro de Chave Pix


class PixKeyCreateInput(BaseModel):
    id_conta: int
    tipo_chave: Literal["CPF", "EMAIL", "TELEFONE", "ALEATORIA"]
    valor_chave: str


class PixCreatedResponse(BaseModel):
    message: str
    id_chave: int
    tipo_chave: str
    valor_chave: str

# 2. Schema para Transferência Pix (via Chave Pix)


class PixTransferInput(BaseModel):
    id_conta_origem: int
    chave_destino: int  # A chave Pix de quem vai receber
    valor: Decimal

    @field_validator("valor")
    def validar_valor(cls, value: Decimal) -> Decimal:
        if value <= Decimal('0.00'):
            raise ValueError(
                "Valor da transação Pix deve ser maior que R$0,00")
        return round(value, 2)


class PixTransferOutput(BaseModel):
    message: str
    id_transacao: int
    valor: Decimal
