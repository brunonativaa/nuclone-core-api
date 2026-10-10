from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_db
from src.modules.account.service import ContaService
from src.modules.account.exceptions import ClienteNaoEncontradoException,ContaNaoEncontradaException
from src.modules.account.schema import (
    AccountCreateInput,
    AccountCreatedResponse,
    AccountBalanceOutput,
    AccountOutput
)

router = APIRouter(prefix="/accounts", tags=["Accounts"])


@router.post("",
response_model=AccountCreatedResponse,  
status_code=status.HTTP_201_CREATED,
)

async def create_account(
    payload: AccountCreateInput, 
    db: AsyncSession = Depends(get_db)
):
    service = ContaService(db)
    try:
        # 1. Executa a regra de negócio na camada de serviço
        nova_conta = await service.create_account(
            id_cliente=payload.id_cliente,
            agencia=payload.agencia,
            tipo_conta=payload.tipo_conta
        )

        # Converte a model do SQLAlchemy para o Schema Pydantic explicitamente
        conta_dto = AccountOutput.model_validate(nova_conta)

        return AccountCreatedResponse(
            message="Conta bancária criada com sucesso!",
            account= conta_dto
        )
        
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


@router.get(
    "/{id_conta}", 
    status_code=status.HTTP_200_OK
)
async def get_account_by_id(
    id_conta: int, 
    db: AsyncSession = Depends(get_db)
):
    service = ContaService(db)
    try:
        # Garante que o retorno seja validado pelo response_model (AccountOutput)
        conta = await service.get_by_id(id_conta)
        return AccountOutput.model_validate(conta)
    except ContaNaoEncontradaException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "code": "ACCOUNT_NOT_FOUND",
                "message": str(e),
                "id_conta": id_conta,         
            },
        )


@router.get(
    "/{id_conta}/balance", 
    status_code=status.HTTP_200_OK, 
    response_model=AccountBalanceOutput
)
async def get_account_balance(
    id_conta: int, 
    db: AsyncSession = Depends(get_db)
):

    service = ContaService(db)
    try:
        return await service.get_balance(id_conta)
    except ContaNaoEncontradaException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "code": "ACCOUNT_NOT_FOUND",
                "message": str(e),
                "id_conta": id_conta,
            },
        )
