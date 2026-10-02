from datetime import datetime, timedelta, timezone
from typing import Optional
import bcrypt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.core.config import settings
from src.core.database import get_db
from src.modules.customer.model import ClienteModel

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# --- GERENCIAMENTO DE SENHAS (NATIVO BCRYPT) ---


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Valida a senha fornecida contra o hash armazenado no banco."""
    if not plain_password or not hashed_password:
        return False
    try:
        # bcrypt trabalha com bytes; convertemos as strings em UTF-8
        password_bytes = plain_password.encode("utf-8")
        hash_bytes = hashed_password.encode("utf-8")
        return bcrypt.checkpw(password_bytes, hash_bytes)
    except (ValueError, TypeError):
        return False


def hash_password(password: str) -> str:
    """Gera o hash seguro da senha usando o algoritmo Bcrypt."""
    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode("utf-8")


# --- GERENCIAMENTO DE TOKENS JWT ---


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Gera um token JWT contendo as claims fornecidas."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + \
            timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# --- INJEÇÃO DE DEPENDÊNCIA DE AUTENTICAÇÃO ---


async def get_current_customer(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> ClienteModel:
    """Valida o token JWT e retorna o cliente autenticado."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        cpf: str = payload.get("sub")
        if not cpf:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Higieniza o CPF garantindo busca estrita apenas por dígitos
    cpf_limpo = "".join(filter(str.isdigit, str(cpf)))

    # Executa a busca assíncrona
    query = select(ClienteModel).where(ClienteModel.cpf == cpf_limpo)
    result = await db.execute(query)
    cliente = result.scalar_one_or_none()

    if cliente is None:
        raise credentials_exception

    return cliente
