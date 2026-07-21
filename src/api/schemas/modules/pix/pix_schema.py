from pydantic import BaseModel, validator


class PixRequestInput(BaseModel):
    id_conta_origem: int
    id_conta_destino: int
    valor: float

    @validator("valor")
    def validar_valor(cls, value):
        if value <= 0:
            raise ValueError("Valor do Pix deve ser maior que zero")
        return value
