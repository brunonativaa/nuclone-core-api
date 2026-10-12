from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import get_db

from src.modules.customer.service import (
     ClienteService, ClienteJaExisteException, ClienteNaoEncontradoException
)

from src.modules.customer.schema import ClienteCreateInput, ClienteResponse

router = APIRouter(tags=["Clientes"])


@router.post("",response_model=ClienteResponse, status_code=status.HTTP_201_CREATED)
async def create_customer(cliente: ClienteCreateInput, db: AsyncSession = Depends(get_db)):
    service = ClienteService(db)

    try:

        novo_cliente = await service.create_customer(cliente)
        return ClienteResponse.model_validate(novo_cliente)

    except ClienteJaExisteException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": "CLIENT_ALREADY_EXISTS",
                "message": str(e),
            },
        )

@router.get("/{id_cliente}", status_code=status.HTTP_200_OK)
async def get_customer_by_id(id_cliente: int, db: AsyncSession = Depends(get_db)):
    service = ClienteService(db)
    try:
        return await service.get_by_id(id_cliente)
    except ClienteNaoEncontradoException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "code": "CLIENT_NOT_FOUND",
                "message": str(e),
                "id_cliente": id_cliente,
            },
        )
