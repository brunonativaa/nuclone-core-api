from pydantic import BaseModel, Field
from typing import Optional


class RegistrarAuthSchema(BaseModel):
    """Payload enviado no momento do cadastro inicial do usuário"""
    id_cliente: int
    senha_hash: str = Field(..., min_length=8,
                       description="Senha de acesspo do app")
    pin_transacao_hash: Optional[str] = Field(
        None, pattern=r'^\d{4}$', description="PIN de transação do app")


class LoginSchema(BaseModel):
    """Payload para autenticação e geração do Bearer Token"""
    cpf: str = Field(..., pattern=r'^\d{11}$', description="CPF do cliente")
    senha_hash: str


class PinVerificationSchema(BaseModel):
    """Payload para assinar e autorizar transações Pix ou saques"""
    pin_transacao_hash: str = Field(...,
                               pattern=r'^\d{4}$', description="PIN de transação do app")


class TokenSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"
