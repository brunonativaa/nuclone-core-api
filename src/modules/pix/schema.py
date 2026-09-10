from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
from src.core.schema import BaseDTO
from decimal import Decimal
from typing import Literal, Optional


# 1. Schema para Cadastro de Chave Pix


class PixKeyCreateInput(BaseDTO):
    id_conta: int = Field(..., description="Indentificador único do conta")
    tipo_chave: Literal["CPF", "EMAIL", "TELEFONE", "ALEATORIA"] = Field(
        ..., description="Tipo da chave Pix cadastrada"
    )
    valor_chave: str = Field(
        ..., min_length=3, max_length=140, description="Valor da chave Pix"
    )


class PixCreatedResponse(BaseDTO):
    message: str = Field(
        default="Chave Pix cadastrada com sucesso.",
        description="Mensagem de confirmação",
    )
    id_chave: int = Field(
        ..., description="Identificador único da chave criada"
    )
    tipo_chave: str = Field(..., description="Tipo da chave Pix")
    valor_chave: str = Field(..., description="Valor cadastrado da chave")

# 2. Schema para Transferência Pix (via Chave Pix ou ID)


class PixTransferInput(BaseDTO):
    id_conta_origem: int = Field(
        ..., gt=0, description="ID da conta remetente do Pix"
    )
    id_conta_destino: Optional[int] = Field(
        default=None, gt=0, description="ID da conta de destino (opcional)"
    )
    chave_destino: Optional[str] = Field(
        default=None, description="Chave Pix do destinatário (opcional)"
    )
    valor: Decimal = Field(
        ..., gt=Decimal("0.00"), description="Valor financeiro a ser enviado"
    )

    @field_validator("valor")
    @classmethod
    def validar_precisao_valor(cls, value: Decimal) -> Decimal:
        """Garante arredondamento monetário em 2 casas decimais."""
        return round(value, 2)

    @model_validator(mode="after")
    def validar_destino_obrigatorio(self) -> "PixTransferInput":
        """Garante que pelo menos um destino (chave ou id_conta) seja informado."""
        if not self.id_conta_destino and not self.chave_destino:
            raise ValueError(
                "É necessário informar o 'id_conta_destino' ou a 'chave_destino'."
            )
        return self


class PixTransferOutput(BaseDTO):
    message: str = Field(
        default="Transferência Pix realizada com sucesso.",
        description="Status da operação",
    )
    id_transacao: int = Field(
        ..., description="Identificador único do comprovante"
    )
    valor: Decimal = Field(..., description="Valor transferido")
