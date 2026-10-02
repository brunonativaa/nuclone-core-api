from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.core.database import get_db_session
from src.core.security import create_access_token, verify_password
from src.modules.auth.schema import LoginSchema, TokenSchema
from src.modules.customer.model import ClienteModel

router = APIRouter(tags=["Autentificação"])


@router.post("/auth/login", response_model=TokenSchema, status_code=status.HTTP_200_OK)
async def login(
    payload: LoginSchema,
    db: AsyncSession = Depends(get_db_session)
):
    # 1. Sanitiza o CPF (remove pontos e traços caso o cliente envie com formatação)
    cpf_limpo = "".join(filter(str.isdigit, payload.cpf))

    # 2. Busca o cliente no banco pelo CPF
    query = select(ClienteModel).where(ClienteModel.cpf == cpf_limpo)
    result = await db.execute(query)
    cliente = result.scalar_one_or_none()

    # Debug temporário no log (pode remover após validar)
    if not cliente:
        print(
            f"[DEBUG AUTH] Usuário com CPF {cpf_limpo} não encontrado no banco.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="CPF ou senha incorretos.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 3. Compara a SENHA TEXTO PURO (do payload) com o HASH (do banco de dados)
    # ATENÇÃO: verify_password(senha_plana, hash_do_banco)
    senha_valida = verify_password(
        plain_password=payload.senha,
        hashed_password=cliente.senha_hash
    )

    if not senha_valida:
        print(f"[DEBUG AUTH] Senha incorreta para o CPF {cpf_limpo}.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="CPF ou senha incorretos.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 4. Sucesso: Gera o JWT
    access_token = create_access_token(data={"sub": str(cliente.cpf)})
    return TokenSchema(access_token=access_token, token_type="bearer")
