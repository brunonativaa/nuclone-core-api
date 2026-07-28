from fastapi import APIRouter
from src.api.schemas.pix_schema import PixRequestInput

router = APIRouter()


@router.post("/pix/transferir")
def realizar_pix(pix: PixRequestInput):
    return {"mensagem": f"Transferência Pix de R${pix.valor} realizado com sucesso!"}
