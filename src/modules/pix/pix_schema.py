from pydantic import BaseModel, field_validator
from decimal import Decimal

class PixRequestInput(BaseModel):
    id_conta_origem: int
    id_conta_destino: int
    valor: Decimal

    @field_validator("valor")
    def validar_valor(cls, value: Decimal) -> Decimal:
        if value <= Decimal('0,00'):
            raise ValueError("Valor da transação Pix deve ser maior que R$0,00")
        return round(value, 2)
