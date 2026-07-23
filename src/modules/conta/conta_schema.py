from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime

class ContaResponse(BaseModel):
    id_conta: int
    num_conta: str
    tipo_conta: str
    agencia: str = "0001"
    saldo_disponivel: Decimal
    criado_em : datetime

    class Config:
        from_attributes = True
        