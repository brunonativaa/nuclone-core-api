from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.services.customer_service import ClienteService, ClienteJaExisteException, ClienteNaoEncontradoException
from src.api.schemas.customer_schema import ClienteCreateInput, ClienteOutput

router = APIRouter(tags=["Customers"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_customer(cliente: ClienteCreateInput, db: Session = Depends(get_db)):
    service = ClienteService(db)

    try:
        new_customer = service.create_customer(cliente.model_dump())

        return {
            "message": "Cliente cadastrado com sucesso!",
            "customer": {
                "id_cliente": new_customer.id_cliente,
                "nome": new_customer.nome,
                "cpf": new_customer.cpf,
                "email": new_customer.email
            }
        }

    except ClienteJaExisteException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/{id_cliente}", status_code=status.HTTP_200_OK)
def get_customer_by_id(id_cliente: int, db: Session = Depends(get_db)):
    service = ClienteService(db)
    try:
        return service.get_by_id(id_cliente)
    except ClienteNaoEncontradoException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e))
