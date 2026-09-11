from unittest.mock import MagicMock
import pytest
from src.modules.account.schema import AccountCreateInput
from src.modules.account.service import (
    ContaNaoEncontradaException,
    ContaService,
)


@pytest.fixture
def db_session_mock(mocker):
    """Cria um mock genérico da sessão do SQLAlchemy."""
    session = mocker.MagicMock()
    return session


@pytest.fixture
def account_service_mocked(db_session_mock):
    """Instancia o ContaService injetando mocks nos repositórios para isolamento unitário."""
    service = ContaService(db_session_mock)
    service.conta_repo = MagicMock()
    service.cliente_repo = MagicMock()
    return service


def test_create_account_rollback_on_exception(
    db_session_mock, account_service_mocked
):
    # 1. Simula cliente existente no banco
    account_service_mocked.cliente_repo.get_by_id.return_value = MagicMock(
        id_cliente=1
    )
    account_service_mocked.conta_repo.create_account.return_value = (
        MagicMock(id_conta=1)
    )

    # 2. Força falha na criação do saldo para validar acionamento do rollback
    account_service_mocked.conta_repo.create_saldo.side_effect = Exception(
        "Erro na transação de banco"
    )

    dados = AccountCreateInput(id_cliente=1, tipo_conta="PF")

    # 3. Executa esperando a exceção
    with pytest.raises(Exception):
        account_service_mocked.create_account(dados)

    # 4. Garante que o rollback da sessão simulada foi invocado
    db_session_mock.rollback.assert_called_once()


def test_get_by_id_conta_nao_encontrada(account_service_mocked):
    # Simula busca que não encontra o registro
    account_service_mocked.conta_repo.search_account.return_value = None

    with pytest.raises(ContaNaoEncontradaException):
        account_service_mocked.get_by_id(999)
