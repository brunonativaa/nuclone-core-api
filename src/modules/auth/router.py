from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.core.database import get_db_session 
from src.core.security import create_access_token, verify_password
from src.modules.auth.schema import TokenSchema
from src.modules.customer.model import ClienteModel

router = APIRouter(tags=["Auth"])


@router.post("/auth/login", response_model=TokenSchema, status_code=status.HTTP_200_OK)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db_session)
):
    """Endpoint para autenticação de clientes"""
    query = select(ClienteModel).where(ClienteModel.email == form_data.username)
    result = await db.execute(query)
    cliente = result.scalar()

    if not cliente or not verify_password(form_data.password, cliente.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )

    claims = {
        "sub": str(cliente.id_cliente),
        "role": cliente.role,
        "email": cliente.email
    }

    access_token = create_access_token(data=claims)
    return TokenSchema(access_token=access_token, token_type="bearer")