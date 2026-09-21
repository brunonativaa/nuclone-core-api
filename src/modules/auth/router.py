from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.security import verify_password, create_access_token
from src.modules.auth.schema import LoginSchema, TokenSchema


router =  APIRouter()

def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    # 1. Consulta o usuário/conta no banco (exemplo conceitual)
    # user = user_repository.get_by_cpf(form_data.username)
    # if not user or not verify_password(form_data.password, user.senha_hash):
    #     raise HTTPException(status_code=401, detail="Credenciais inválidas.")

    # Simulação de ID localizado
    id_conta_autenticada = 1 

    # 2. Emite o JWT injetando o ID na claim 'sub'
    access_token = create_access_token(data={"sub": str(id_conta_autenticada)})
    return {"access_token": access_token, "token_type": "bearer"}
