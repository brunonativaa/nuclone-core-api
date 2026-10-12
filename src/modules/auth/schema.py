from pydantic import BaseModel, Field, EmailStr
from typing import Optional


class RegistrarAuthSchema(BaseModel):
    """Payload enviado no cadastro das credenciais de acesso."""

    id_cliente: int = Field(...,
                            description="ID do cliente cadastrado no sistema")
    senha: str = Field(
        ...,
        min_length=8,
        max_length=64,
        description="Senha em texto puro enviada via HTTPS"
    )
    pin_transacao: Optional[str] = Field(
        None,
        pattern=r"^\d{4}$",
        description="PIN de transação com exatamente 4 dígitos numéricos"
    )


class LoginSchema(BaseModel):
    """Payload para autenticação via JSON (alternativo ou padrão para API mobile)."""

    cpf: str = Field(..., pattern=r"^\d{11}$",
                     description="CPF do cliente (somente números)")
    senha: str = Field(..., description="Senha do cliente em texto puro")


class PinVerificationSchema(BaseModel):
    """Payload para autorizar transações sensíveis (Pix/Saque)."""

    pin_transacao: str = Field(
        ...,
        pattern=r"^\d{4}$",
        description="PIN de 4 dígitos numéricos enviado pelo usuário"
    )


class TokenSchema(BaseModel):
    """Resposta com o Token de Acesso JWT."""

    access_token: str = Field(..., description="Token JWT codificado")
    token_type: str = Field(
        "bearer", description="Tipo do token de autorização")
