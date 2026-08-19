from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.services.account_service import (
    ContaService, ClienteNaoEncontradoException, ContaNaoEncontradaException)
from src.api.schemas.account_schema import (
    AccountCreateInput,
    AccountCreatedResponse,
    AccountBalanceOutput
)

router = APIRouter(tags=["Accounts"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=AccountCreatedResponse)
def create_account(payload: AccountCreateInput, db: Session = Depends(get_db)):
    service = ContaService(db)
    try:
        new_account = service.create_account(payload.model_dump())
        return {
            "message": "Conta bancária criada com sucesso!",
            "account": new_account
        }
    except ClienteNaoEncontradoException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "code": "CLIENT_NOT_FOUND",
                "message": str(e),
                "id_cliente": payload.id_cliente,
            },
        )


@router.get("/{id_conta}", status_code=status.HTTP_200_OK, response_model=AccountBalanceOutput)
def get_account_balance(id_conta: int, db: Session = Depends(get_db)):
    service = ContaService(db)
    try:
        balance_info = service.get_saldo(id_conta)
        return balance_info
    except ContaNaoEncontradaException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "Conta Não Encontrada",
                "message": f"O id da conta {id_conta} não foi encontrado",
                "account_id": id_conta
            },
        )
