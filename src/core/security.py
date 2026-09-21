from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext


SECRET_KEY = "bdsovijrkldlhrgejndsmklçjkdfdserg"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# --- GERENCIAMENTO DE SENHAS ---

def hash_password(password: str) -> str:
    """Gera o hash seguro da senha usando o algoritmo Bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Valida a senha fornecida contra o hash armazenado no banco."""
    return pwd_context.verify(plain_password, hashed_password)


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

# --- INJEÇÃO DE DEPENDÊNCIA DE AUTORIZAÇÃO ---

def get_current_user_id(token: str = Depends(oauth2_scheme)) -> int:
    """
    Intercepta a requisição, extrai o Bearer token do header,
    valida a assinatura JWT e retorna o id_conta autenticado.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais de acesso.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id_str: str = payload.get("sub")
        if user_id_str is None:
            raise credentials_exception
        return int(user_id_str)
    except (JWTError, ValueError):
        raise credentials_exception