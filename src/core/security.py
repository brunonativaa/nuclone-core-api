from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.core.config import settings
from src.core.database import get_db
from src.modules.customer.model import ClienteModel


SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


# --- GERENCIAMENTO DE SENHAS ---


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Valida a senha fornecida contra o hash armazenado no banco."""
    if not hashed_password:
        return False
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except ValueError:
        # Evita exceções caso a string gravada no banco não seja um hash válido
        return False

def hash_password(password: str) -> str:
    """Gera o hash seguro da senha usando o algoritmo Bcrypt."""
    return pwd_context.hash(password)


# --- GERENCIAMENTO DE TOKENS JWT ---

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Gera um token JWT contendo as claims fornecidas (ex: sub contendo o id_conta)."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
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
        id_cliente: str = payload.get("sub")
        if id_cliente is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    query = select(ClienteModel).where(ClienteModel.id_cliente == int(id_cliente))
    result = await db.execute(query)
    cliente = result.scalar()

    if cliente is None:
        raise credentials_exception

    return cliente