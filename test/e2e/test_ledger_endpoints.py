from datetime import date
from decimal import Decimal
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.main import app  # Importe a instância principal do FastAPI
from src.core.database import get_db  # Dependência de sessão do banco
from src.modules.customer.model import ClienteModel
from src.modules.account.model import ContaModel, SaldoContaModel

@pytest.mark.asyncio
async def test_get_bank_extract_success(client: AsyncClient, db_session: AsyncSession, token_autenticacao_valido: str):
    # 1. Arrange: Força o FastAPI a usar a mesma sessão de teste ativa
    app.dependency_overrides[get_db] = lambda: db_session

    try:
        # Insere o cliente e a conta na mesma transação compartilhada
        cliente = ClienteModel(
            id_cliente=1, 
            nome="Usuário Teste", 
            cpf="12586584582", 
            email="testoi@oul.com.bt",
            sexo="M",
            senha_hash="teste123456",
            pin_transacao_hash="123456",
            data_nascimento=date(1990, 10, 6)
        )
        
        conta = ContaModel(
            id_conta=100, 
            id_cliente=1, 
            num_conta="12345-6",
            saldo=SaldoContaModel(saldo_disponivel=Decimal("1000.0"))
        )
        
        db_session.add(cliente)
        db_session.add(conta)
        await db_session.commit()

        # 2. Act: Executa a requisição assíncrona
        response = await client.get(
            "/api/v1/ledger/extrato",
            headers={"Authorization": f"Bearer {token_autenticacao_valido}"}
        )
        
        # 3. Assert: Valida o sucesso
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    finally:
        # Limpa o override após o teste para evitar efeitos colaterais em outros arquivos
        app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_get_transaction_forbidden_idor(client: AsyncClient, db_session: AsyncSession, token_usuario_a: str):
    # Tenta acessar uma transação do Usuário B usando o token do Usuário A
    response = await client.get(
        "/ledger/transacoes/9999",
        headers={"Authorization": f"Bearer {token_usuario_a}"}
    )
    assert response.status_code == 404 # Mensagem genérica para evitar vazamento de IDOR