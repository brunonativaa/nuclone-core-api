from pydantic import BaseModel, validator


class ClienteCreateInput(BaseModel):
    nome: str
    cpf:  str
    email: str
    senha: str

    @validator("cpf")
    def validar_cpf(cls, value):
        if len(value) != 11 or not value.isdigit():
            raise ValueError("CPF deve conter exatamente 11 dígitos")
        return value
