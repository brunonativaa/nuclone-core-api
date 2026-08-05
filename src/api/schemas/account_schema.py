from pydantic import BaseModel, Field
from decimal import Decimal
from datetime import datetime


class AccountCreateInput(BaseModel):
    id_cliente: int = Field(...,
                            description="ID do cliente proprietário da conta")
    tipo_conta: str = Field(default="PF", min_length=2,
                            max_length=2, description="Tipo da conta: PF ou PJ")
    agencia: str = Field(default="0001", min_length=4,
                         max_length=4, description="Número da agência bancária")


class AccountOutput(BaseModel):
    id_conta: int
    id_cliente: int
    num_conta: str
    tipo_conta: str
    agencia: str

    class Config:
        from_attributes = True


class AccountCreatedResponse(BaseModel):
    message: str
    account: AccountOutput


class AccountBalanceOutput(BaseModel):
    id_conta: int
    saldo_disponivel: Decimal

    class Config:
        from_attributes = True
