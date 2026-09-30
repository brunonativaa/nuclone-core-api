from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.security import create_access_token, verify_password
from src.modules.auth.schema import TokenSchema

router = APIRouter(tags=["Auth"])


@router.post("/auth/login", response_model=TokenSchema, status_code=status.HTTP_200_OK)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Endpoint OAuth2 compatível com o Swagger UI e clientes HTTP.
    Recebe os campos 'username' e 'password' via Form Data.
    """
    # Exemplo de validação local para testes de integração
    # Em produção: buscar usuário pelo CPF/E-mail no banco e comparar hash
    if form_data.username != "admin" or form_data.password != "123456":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Injeta o identificador da conta no claim 'sub' do JWT
    id_conta = 1
    access_token = create_access_token(data={"sub": str(id_conta)})

    return TokenSchema(access_token=access_token, token_type="bearer")