from pydantic import BaseModel


class ContaResponse(BaseModel):
    id_conta: int
    num_conta: str
    tipo_conta: str
    agencia: str
    saldo_disponivel: float
