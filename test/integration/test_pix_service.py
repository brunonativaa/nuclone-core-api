import pytest
from decimal import Decimal
from src.modules.account.model import ContaModel
from src.modules.pix.service import (
    PixService,
    SaldoInsuficienteException,
    ContaNaoEncontradaException
)


def test_perform_pix_nonexistent_source_account(db_session, id_conta_destino):
    service = PixService(db_session)
    with pytest.raises(ContaNaoEncontradaException, match="Conta de origem não encontrada."):
        service.make_pix_payment(999999, id_conta_destino, Decimal("50.00"))


def test_perform_pix_nonexistent_destination_account(db_session, id_conta_origem):
    service = PixService(db_session)
    with pytest.raises(ContaNaoEncontradaException, match="Conta de destino não encontrada"):
        service.make_pix_payment(id_conta_origem, 999999, Decimal("50.00"))


def test_perform_pix_same_account(db_session, id_conta_origem):
    service = PixService(db_session)
    with pytest.raises(ValueError, match="Não é possível realizar transferência PIX para a mesma conta."):
        service.make_pix_payment(
            id_conta_origem, id_conta_origem, Decimal("50.00"))


def test_adding_balance_invalid_value(db_session, id_conta_origem):
    service = PixService(db_session)
    with pytest.raises(ValueError, match="O valor adicionado deve ser maior que zero."):
        service.adding_balance(id_conta_origem, Decimal("-10.00"))


def test_adding_balance_nonexistent_account(db_session):
    service = PixService(db_session)
    with pytest.raises(ContaNaoEncontradaException, match="Conta não encontrada."):
        service.adding_balance(999999, Decimal("100.00"))


def test_perform_pix_failure_bank_rollback(db_session, id_conta_origem, id_conta_destino, mocker):
    service = PixService(db_session)
    service.adding_balance(id_conta_origem, 250.00)

    mocker.patch.object(service.pix_repo, "record_transaction",
                        side_effect=Exception("Erro forçado do banco"))

    with pytest.raises(Exception, match="Erro forçado do banco"):
        service.make_pix_payment(
            id_conta_origem, id_conta_destino, Decimal("50.00"))

# Validates the account deposit transaction


def test_adding_balance_to_account(db_session, id_conta_origem):
    service = PixService(db_session)

    saldo_incial = service.conta_repo.get_saldo(
        id_conta_origem).saldo_disponivel
    service.adding_balance(id_conta_origem, 250.00)

    saldo_final = service.conta_repo.get_saldo(
        id_conta_origem).saldo_disponivel
    assert saldo_final == saldo_incial + Decimal("250.00")


def test_successfully_complete_a_pix_transfer(db_session, id_conta_origem, id_conta_destino):
    service = PixService(db_session)

    saldo_inicial_origem = service.conta_repo.get_saldo(
        id_conta_origem).saldo_disponivel

    service.adding_balance(id_conta_origem, 250.00)

    transacao = service.make_pix_payment(
        id_conta_origem, id_conta_destino, 50.00)

    assert transacao.valor == Decimal("50.00")

    saldo_origem = service.conta_repo.get_saldo(
        id_conta_origem).saldo_disponivel
    saldo_destino = service.conta_repo.get_saldo(
        id_conta_destino).saldo_disponivel

    assert saldo_origem == saldo_inicial_origem + Decimal("200.00")
    assert saldo_destino == Decimal("50.00")


def test_pix_insufficient_funds(db_session, id_conta_origem, id_conta_destino):
    service = PixService(db_session)

    saldo_inicial_origem = service.conta_repo.get_saldo(
        id_conta_origem).saldo_disponivel

    with pytest.raises(SaldoInsuficienteException):
        service.make_pix_payment(id_conta_origem, id_conta_destino, 1000.00)

    saldo_origem = service.conta_repo.get_saldo(
        id_conta_origem).saldo_disponivel
    saldo_destino = service.conta_repo.get_saldo(
        id_conta_destino).saldo_disponivel

    assert saldo_origem == saldo_inicial_origem
    assert saldo_destino == Decimal("0.00")
