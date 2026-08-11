from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.services.pix_service import (
    PixService, SaldoInsuficienteException, ContaNaoEncontradaException)


from src.api.schemas.pix_schema import PixTransferInput, PixTransferOutput

router = APIRouter(prefix="/pix", tags=["Pix Transactions"])


@router.post("/transferir", status_code=status.HTTP_200_OK, response_model=PixTransferOutput)
def transfer_pix(payload: PixTransferInput, db: Session = Depends(get_db)):
    service = PixService(db)
    try:
        transaction = service.realizar_pix(
            id_conta_origem=payload.id_conta_origem,
            id_conta_destino=payload.id_conta_destino,
            valor=payload.valor
        )
        return PixTransferOutput(
            message="Transferência PIX realizada com sucesso!",
            id_transacao=transaction.id_transacao,
            valor=payload.valor
        )
    except (SaldoInsuficienteException, ContaNaoEncontradaException) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
