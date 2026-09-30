from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.modules.account.service import (
    ContaService, ClienteNaoEncontradoException, ContaNaoEncontradaException)
from src.modules.account.schema import (
    AccountCreateInput,
    AccountCreatedResponse,
    AccountBalanceOutput,
    AccountOutput
)

router = APIRouter(prefix="/accounts", tags=["Accounts"])


@router.post("",response_model=AccountCreatedResponse,  status_code=status.HTTP_201_CREATED,)
def create_account(payload: AccountCreateInput, db: Session = Depends(get_db)):
    service = ContaService(db)
    try:
        # 1. Executa a regra de negócio na camada de serviço
        new_account = service.create_account(payload)

        # Converte a model do SQLAlchemy para o Schema Pydantic explicitamente
        account_dto = AccountOutput.model_validate(new_account)

        return {
            "message": "Conta bancária criada com sucesso!",
            "account": account_dto
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
# Adicione a busca por ID no router


@router.get("/{id_conta}", status_code=status.HTTP_200_OK)
def get_account_by_id(id_conta: int, db: Session = Depends(get_db)):
    service = ContaService(db)
    try:
        # Garanta que exista o método get_by_id no seu ContaService
        return service.get_by_id(id_conta)
    except ContaNaoEncontradaException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": f"Conta {id_conta} não encontrada"}
        )


@router.get("/{id_conta}/balance", status_code=status.HTTP_200_OK, response_model=AccountBalanceOutput)
def get_account_balance(id_conta: int, db: Session = Depends(get_db)):
    service = ContaService(db)
    try:
        return service.get_saldo(id_conta)
    except ContaNaoEncontradaException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "Conta Não Encontrada",
                "message": f"O id da conta {id_conta} não foi encontrado",
                "account_id": id_conta
            },
        )
