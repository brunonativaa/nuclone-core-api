from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.modules.pix.service import (
    PixService,
    SaldoInsuficienteException,
    ContaNaoEncontradaException,
)
from src.modules.pix.schema import (
    PixTransferInput,
    PixTransferOutput,
    PixKeyCreateInput,
)

router = APIRouter(tags=["Pix Transactions"])


@router.post("/transfer", status_code=status.HTTP_200_OK, response_model=PixTransferOutput)
def transfer_pix(payload: PixTransferInput, db: Session = Depends(get_db)):
    service = PixService(db)
    try:
        transaction = service.make_pix_payment(
            id_conta_origem=payload.id_conta_origem,
            chave_destino=payload.chave_destino,  # Recebe a chave PIX string
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
def create_pix_key(payload: PixKeyCreateInput, db: Session = Depends(get_db)):
    service = PixService(db)

    try:
        new_key = service.register_pix_key(
            id_conta=payload.id_conta,
            key_type=payload.tipo_chave,
            valor_chave=getattr(payload, 'valor_chave', None)
        )
        return {
            "message": "Chave Pix Cadastrada com sucesso!",
            "id_chave": new_key.id_chave,
            "valor_chave": new_key.valor_chave
        }
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
