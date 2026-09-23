from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict, model_validator


class LimitesResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_conta: int = Field(
        ..., 
        gt=0, 
        description="Identificador único da conta bancária",
        json_schema_extra={"example": 10458}
    )
    limite_diario: Decimal = Field(
        ..., 
        ge=0, 
        max_digits=12, 
        decimal_places=2, 
        description="Limite total disponível para o período diurno",
        json_schema_extra={"example": "5000.00"}
    )
    limite_noturno: Decimal = Field(
        ..., 
        ge=0, 
        max_digits=12, 
        decimal_places=2, 
        description="Limite total disponível para o período noturno",
        json_schema_extra={"example": "1000.00"}
    )
    limite_diario_utilizado: Decimal = Field(
        ..., 
        ge=0, 
        max_digits=12, 
        decimal_places=2, 
        description="Valor consumido da cota diurna no ciclo atual",
        json_schema_extra={"example": "350.50"}
    )
    limite_noturno_utilizado: Decimal = Field(
        ..., 
        ge=0, 
        max_digits=12, 
        decimal_places=2, 
        description="Valor consumido da cota noturna no ciclo atual",
        json_schema_extra={"example": "0.00"}
    )


class UpdateLimiteSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    novo_limite_diario: Optional[Decimal] = Field(
        None, 
        ge=0, 
        max_digits=12, 
        decimal_places=2,
        description="Novo limite para o período diurno",
        json_schema_extra={"example": "3000.00"}
    )
    novo_limite_noturno: Optional[Decimal] = Field(
        None, 
        ge=0, 
        max_digits=12, 
        decimal_places=2,
        description="Novo limite para o período noturno",
        json_schema_extra={"example": "800.00"}
    )

    @model_validator(mode="after")
    def validar_pelo_menos_um_campo(self) -> "UpdateLimiteSchema":
        """Garante que a requisição de atualização não seja enviada vazia."""
        if self.novo_limite_diario is None and self.novo_limite_noturno is None:
            raise ValueError("Ao menos um limite (diário ou noturno) deve ser informado para atualização.")
        return self