from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.modules.pix.pix_service import (
    PixService, SaldoInsuficienteException, ContaNaoEncontradaException,)
from src.modules.pix.pix_schema import PixTransferInput, PixTransferOutput, PixKeyInput

router = APIRouter(tags=["Pix Transactions"])


@router.post("/transfer", status_code=status.HTTP_200_OK, response_model=PixTransferOutput)
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

    except ContaNaoEncontradaException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)

        )

    except (SaldoInsuficienteException, ValueError) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/keys", status_code=status.HTTP_201_CREATED)
def create_pix_key(payload: PixKeyInput, db: Session = Depends(get_db)):

    service = PixService(db)
    try:
        service.register_pix_key(
            id_conta=payload.id_conta,
            key_type=payload.tipo_chave
        )

        return {"message": "Chave Pix Cadastrada com sucesso!"}

    except ContaNaoEncontradaException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
