import pytest
from datetime import timedelta
from fastapi import HTTPException
from jose import jwt 
from src.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user_id,
    SECRET_KEY,
    ALGORITHM
)


def test_verify_password_success_and_failure():
    password = "SenhaSegura123!"
    hashed = hash_password(password)

    assert verify_password(password, hashed) is True
    assert verify_password("SenhaErrada", hashed) is False


def test_create_acess_token_custom_expire():
    data = {"sub": "123"}
    expires_delta = timedelta(minutes=15)
    token = create_access_token(data=data, expires_delta=expires_delta)

    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert payload.get("sub") == "123"
    assert "exp" in payload

def test_get_current_user_id_success():
    token = create_access_token(data={"sub": "42"})
    user_id = get_current_user_id(token=token)
    assert user_id == 42

def test_get_current_user_id_invalid_token():
    with pytest.raises(HTTPException) as exc_info:
        get_current_user_id(token="token_ivalido_ou_forjado")
    assert exc_info.value.status_code == 401

def test_get_current_user_id_missing_sub_claim():
    token = jwt.encode({"outra_claim": "valor"}, SECRET_KEY, algorithm=ALGORITHM)
    with pytest.raises(HTTPException) as exc_info:
        get_current_user_id(token=token)
    assert exc_info.value.status_code == 401 