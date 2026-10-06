import pytest
import uuid
from httpx import AsyncClient
from datetime import date

from src.modules.auth.repository import AuthRepository
from src.modules.customer.model import ClienteModel
from src.modules.account.model import ContaModel
from src.core.security import  hash_password



async def test_login_credenciais_invalidas(client: AssyncClient):
    # Envia credenciais erradas para disparar a HTTPException das linhas 23-28
    response = await client.post(
        "/api/v1/auth/login",
        data={"username": "usuario_errado", "password": "senha_errada"}
    )
    
    assert response.status_code == 401
    assert response.json()["detail"] == "CPF ou senha invalidos."


async def test_auth_repository_get_cliente_by_cpf(db_session):
    repo = AuthRepository(db_session)
    cliente = ClienteModel(
        nome="Teste Auth",
        cpf="12345678900",
        sexo="F",
        email="auth@test.com",
        senha_hash="hdieuhcdkd",
        pin_transacao_hash="528545",
        data_nascimento=date(1999, 2, 20)
    )

    db_session.add(cliente)
    await db_session.commit()

    resultado = await repo.get_cliente_by_cpf("12345678900")
    assert resultado is not None
    assert resultado.cpf == "12345678900"

    assert await repo.get_cliente_by_cpf("85989985585") is None

async def test_auth_repository_get_account_by_cliente_id(db_session):
    repo = AuthRepository(db_session)
    cliente = ClienteModel( 
        nome="Teste Conta", 
            cpf="10987654321",
            sexo="M",
            email="conta@teste.com",
            senha_hash="kdhownjkcwpjk",
            pin_transacao_hash="123456",
            data_nascimento=date(1992, 1, 12)
)
    db_session.add(cliente)
    await db_session.commit()
    await db_session.refresh(cliente)


    uid = str(uuid.uuid4())[:5]
    conta = ContaModel(
        id_cliente=cliente.id_cliente,
        num_conta=f"000{uid}-1",
        agencia="0001",
        tipo_conta="PF"
    )

    db_session.add(conta)
    await db_session.commit()
    await db_session.refresh(conta)

    # 3. Executa a busca no repositorio
    resultado = await repo.get_account_by_cliente_id(cliente.id_cliente)
    
    # Assertivas
    assert resultado is not None
    assert resultado.id_cliente == cliente.id_cliente

    # Teste de id inexistente
    assert await repo.get_account_by_cliente_id(99999) is None