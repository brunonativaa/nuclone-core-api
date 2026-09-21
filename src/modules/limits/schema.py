from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field

class LimitsResponseSchema(BaseModel):
    id_conta: int
    limite_diario: Decimal
    limite_noturno: Decimal
    limite_diario_utilizado: Decimal
    limite_noturno_utilizado: Decimal

class UpdateLimiteSchema(BaseModel):
    novo_limite_diario: Optional[Decimal] = Field(None, gt=0)
    novo_limite_noturno: Optional[Decimal] = Field(None, gt=0)