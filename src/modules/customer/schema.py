import re
from datetime import date
from pydantic import EmailStr, Field, field_validator, ConfigDict
from src.core.schema import BaseDTO
from typing import Optional


class ClienteCreateInput(BaseDTO):

    model_config = ConfigDict(from_attributes=True)
    nome: str = Field(..., min_length=3, max_length=100,
                      description="Nome completo")
    cpf:  str = Field(..., min_length=11, max_length=11,
                      description="CPF sem pontos ou traços(apenas 11 digitos)")
    sexo: Optional[str] = Field(None, min_length=1, max_length=1,
                                description="Sexo do cliente (M/F)")
    email: EmailStr = Field(..., min_length=8, max_length=100,
                            description="E-mail válido do cliente")
    senha_hash: str = Field(..., min_length=8, max_length=60,
                            description="Senha hash em texto puro para cadastro do cliente")
    pin_transacao_hash: str = Field(..., min_length=4, max_length=6,
                                    description="PIN de transação de 4 a 6 dígitos em texto puro para cadastro do cliente")
    data_nascimento: date = Field(...,
                                  description="Data de nascimento formato YYYY-MM-DD")

    @field_validator("cpf")
    @classmethod
    def validar_cpf(cls, value: str) -> str:

        cpf_limpo = re.sub(r'\D', '', value)

        if len(cpf_limpo) != 11:
            raise ValueError("CPF deve conter exatamente 11 dígitos ")
        return cpf_limpo


class ClienteResponse(BaseDTO):
    id_cliente: int = Field(..., description="Indentificador único da conta")
    nome: str = Field(..., description="Nome do cliente")
    cpf: str = Field(...,
                     description="CPF sem pontos ou traços(apenas 11 digitos)")
    email: EmailStr = Field(..., description="E-mail válido do cliente")

    class Config:
        from_attributes = True
