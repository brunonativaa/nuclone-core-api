import re
from pydantic import BaseModel, EmailStr, Field, field_validator


class ClienteCreateInput(BaseModel):
    nome: str = Field(..., min_length=3, max_length=60, description="Nome completo")
    cpf:  str = Field(..., description="CPF sem pontos ou traços(apenas 11 digitos)")
    email: EmailStr = Field(..., description="E-mail válido do cliente")
    senha: str = Field(..., min_length=8, description="Senha de usuario (mínimo 8 caracteres)")

    @field_validator("cpf")
    @classmethod
    def validar_cpf(cls, value: str) -> str:
        cpf_limpo = re.sub(r'\D', '', value)
        if len(cpf_limpo) != 11:
            raise ValueError("CPF deve conter exatamente 11 dígitos")
        return cpf_limpo
