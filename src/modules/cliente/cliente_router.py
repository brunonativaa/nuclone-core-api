from fastapi import APIRouter, HTTPException
from src.modules.cliente.cliente_schema import ClienteCreateInput

router = APIRouter()


@router.post("/clientes", status_code=201)
def criar_cliente(cliente: ClienteCreateInput):
    return {"mensagem": "Cliente criado com sucesso!", "dados": cliente}

