from fastapi import APIRouter
from src.api.schemas.modules.pix.pix_schema import PixRequestInput

router = APIRouter()


@router.post("/")
def realizar_pix(pix: PixRequestInput):
    return {"mensagem": "Pix realizado."}
