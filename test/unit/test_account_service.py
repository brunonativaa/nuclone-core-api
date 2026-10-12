from unittest.mock import MagicMock, AsyncMock
import pytest
from src.modules.account.schema import AccountCreateInput
from src.modules.account.service import (
    ContaNaoEncontradaException,
    ContaService,
)


@pytest.fixture
async def db_session_mock(mocker):
    """Cria um mock genérico da sessão do SQLAlchemy."""
    session = mocker.MagicMock()
    return session


@pytest.fixture
async def account_service_mocked(db_session_mock):
    """Instancia o ContaService injetando mocks nos repositórios para isolamento unitário."""
    service = ContaService(db_session_mock)
    service.conta_repo = MagicMock()
    service.cliente_repo = MagicMock()
    return service

@pytest.mark.asyncio
async def test_create_account_rollback_on_exception(account_service_mocked):
    # 1. Garantir que os métodos chamados dentro de create_account sejam AsyncMock
    account_service_mocked.conta_repo.create_account = AsyncMock(
        side_effect=Exception("Erro de Banco")
    )
    
    # Se o serviço valida o cliente antes de criar a conta, mocke a resposta do cliente_repo também:
    account_service_mocked.cliente_repo.get_by_id = AsyncMock(return_value={"id": 1})

    dados = AccountCreateInput(id_cliente=1, tipo_conta="PF")

    # 2. Execução e asserção
    with pytest.raises(Exception) as exc_info:
        await account_service_mocked.create_account(dados)

    # 3. Verifica se a exceção gerada foi exatamente a do side_effect
    assert "Erro de Banco" in str(exc_info.value)

    dados = AccountCreateInput(id_cliente=1, tipo_conta="PF")

    # 2. Execução e asserção
    with pytest.raises(Exception) as exc_info:
        await account_service_mocked.create_account(dados)

    # 3. Verifica se a exceção gerada foi exatamente a do side_effect
    assert "Erro de Banco" in str(exc_info.value)

@pytest.mark.asyncio
async def test_get_by_id_conta_nao_encontrada():
    # 1. Cria o mock assíncrono para o repositório de contas
    mock_account_repo = AsyncMock()
    
    # 2. Configura o método assíncrono para retornar None (simulando conta inexistente)
    mock_account_repo.get_account_by_id.return_value = None

    # 3. Injeta o mock no ContaService
    account_service = ContaService(db_session=None, conta_repo=mock_account_repo)

    # 4. Asserção da exceção de domínio esperada
    with pytest.raises(ContaNaoEncontradaException):
        await account_service.get_by_id(id_conta=999)

    # 5. Valida a chamada do repositório
    mock_account_repo.get_account_by_id.assert_called_once_with(999)