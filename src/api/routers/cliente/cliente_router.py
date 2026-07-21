from fastapi import APIRouter
from src.api.schemas.modules.cliente.cliente_schema import ClienteCreateInput

router = APIRouter()


@router.post("/")
def criar_cliente(cliente: ClienteCreateInput):
    return {"mensagem": "Cliente criado com sucesso!"}
