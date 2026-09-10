from pydantic import BaseModel, ConfigDict, Field
from src.core.schema import BaseDTO
from decimal import Decimal
from datetime import datetime


class AccountCreateInput(BaseDTO):
    id_cliente: int = Field(...,
                            description="ID do cliente proprietário da conta")
    tipo_conta: str = Field(default="PF", min_length=2,
                            max_length=2, description="Tipo da conta: PF ou PJ")
    agencia: str = Field(default="0001", min_length=4,
                         max_length=4, description="Número da agência bancária")


class AccountOutput(BaseDTO):

    id_conta: int = Field(..., description="Indentificador único da conta")
    id_cliente: int = Field(..., decimal_places="ID do cliente proprietário")
    num_conta: str = Field(..., description="Número da conta corrente")
    tipo_conta: str = Field(..., description="Tipo da conta (PF/PJ)")
    agencia: str = Field(..., description="Código da agência")


class AccountCreatedResponse(BaseDTO):
    message: str = Field(..., description="Mensagem de confirmação")
    account: AccountOutput


class AccountBalanceOutput(BaseModel):
    id_conta: int = Field(..., description="Indentificador único da conta")
    saldo_disponivel: Decimal = Field(...,
                                      description="Saldo dispoivel para transação")
