import pytest
from unittest.mock import MagicMock
from src.modules.account.service import (
    ContaService,
    ClienteNaoEncontradoException,
    ContaNaoEncontradaException
)

# 1. Cobre a Linha 23


def test_create_account_cliente_nao_encontrado():
    db_mock = MagicMock()
    service = ContaService(db_mock)
    service.cliente_repo.get_by_id = MagicMock(return_value=None)

    with pytest.raises(ClienteNaoEncontradoException):
        service.create_account({"id_cliente": 999})

# 2. Cobre as Linhas 39-41 (Rollback em caso de falha no banco)


def test_create_account_rollback_on_exception():
    db_mock = MagicMock()
    service = ContaService(db_mock)
    service.cliente_repo.get_by_id = MagicMock(return_value={"id": 1})
    service.conta_repo.create_account = MagicMock(
        side_effect=Exception("Database error"))

    with pytest.raises(Exception):
        service.create_account({"id_cliente": 1})

    db_mock.rollback.assert_called_once()

# 3. Cobre a Linha 49


def test_get_by_id_conta_nao_encontrada():
    db_mock = MagicMock()
    db_mock.query().filter().first.return_value = None
    service = ContaService(db_mock)

    with pytest.raises(ContaNaoEncontradaException):
        service.get_by_id(999)

# 4. Cobre a Linha 52


def test_get_saldo_conta_nao_encontrada():
    db_mock = MagicMock()
    service = ContaService(db_mock)
    service.conta_repo.search_account = MagicMock(return_value=None)

    with pytest.raises(ContaNaoEncontradaException):
        service.get_saldo(999)
