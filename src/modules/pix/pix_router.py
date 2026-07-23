from fastapi import APIRouter
from src.modules.pix.pix_schema import PixRequestInput

router = APIRouter()


@router.post("/pix/transferir")
def realizar_pix(pix: PixRequestInput):
    return {"mensagem": f"Transferência Pix de R${pix.valor} realizado com sucesso!"}
