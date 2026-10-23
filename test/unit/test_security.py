import pytest
from datetime import timedelta, date
from fastapi import HTTPException
from jose import jwt 
from src.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_customer,
    SECRET_KEY,
    ALGORITHM
)
from src.modules.customer.model import ClienteModel


async def test_verify_password_success_and_failure():
    password = "SenhaSegura123!"
    hashed = hash_password(password)

    assert verify_password(password, hashed) is True
    assert verify_password("SenhaErrada", hashed) is False


async def test_create_access_token_with_custom_expire():
    data = {"sub": "1"}
    expires_delta = timedelta(minutes=15)
    token = create_access_token(data=data, expires_delta=expires_delta)

    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert payload.get("sub") == "1"
    assert "exp" in payload

async def test_create_access_token_default_expires():
    data = {"sub": "1"}
    token = create_access_token(data=data)
    
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert payload.get("sub") == "1"

@pytest.mark.asyncio
async def test_get_current_customer_id_success(db_session: AsyncSession):
    # 1. Arrange: Insere um cliente na base de dados em memória cujo ID corresponde ao 'sub' do token
    cliente = ClienteModel(
        id_cliente=1,
        nome="Utilizador Teste Security",
        cpf="12345678901",
        email="security@fintech.com",
        senha_hash="fake_hash",
        pin_transacao_hash="123456",
        sexo="M",
        data_nascimento=date(1990, 8, 10)
    )
    db_session.add(cliente)
    await db_session.commit()

    # 2. Act: Gera o token e chama o serviço de autenticação passando a sessão de teste
    token = create_access_token(data={"sub": "1"})
    customer = await get_current_customer(token=token, db=db_session)

    # 3. Assert: Valida que o objeto retornado corresponde ao cliente esperado
    assert customer is not None
    assert customer.id_cliente == 1
    assert customer.email == "security@fintech.com"

@pytest.mark.asyncio
async def test_get_current_customer_id_invalid_token(db_session: AsyncSession):
    with pytest.raises(HTTPException) as exc_info:
        await get_current_customer(token="token_invalido_ou_forjado", db=db_session)
    assert exc_info.value.status_code == 401


@pytest.mark.asyncio
async def test_get_current_customer_id_missing_sub_claim(db_session: AsyncSession):
    token = jwt.encode({"outra_claim": "valor"}, SECRET_KEY, algorithm=ALGORITHM)
    with pytest.raises(HTTPException) as exc_info:
        await get_current_customer(token=token, db=db_session)
    assert exc_info.value.status_code == 401