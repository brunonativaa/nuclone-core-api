from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.core.database import get_db
from src.core.security import create_access_token, verify_password
from src.modules.auth.schema import LoginSchema, TokenSchema
from src.modules.customer.model import ClienteModel

router = APIRouter(tags=["Autentificação"])


@router.post("/auth/login", response_model=TokenSchema, status_code=status.HTTP_200_OK)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """
    Endpoint de login compatível com OAuth2 / Swagger UI.
    Recebe 'username' (CPF) e 'password' (Senha) via Form Data.
    """
    # O campo 'username' do Swagger receberá o CPF
    cpf_limpo = "".join(filter(str.isdigit, form_data.username))

    query = select(ClienteModel).where(ClienteModel.cpf == cpf_limpo)
    result = await db.execute(query)
    cliente = result.scalar_one_or_none()

    if not cliente or not verify_password(form_data.password, cliente.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="CPF ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": str(cliente.cpf)})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
