import pytest
from decimal import Decimal
from src.models.account_model import ContaModel
from src.services.pix_service import (
    PixService,
    SaldoInsuficienteException
)


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

    service.adding_balance(id_conta_origem, 250.00)

    transacao = service.realizar_pix(
        id_conta_origem, id_conta_destino, 50.00)

    assert transacao.valor == Decimal("50.00")

    saldo_origem = service.conta_repo.get_saldo(
        id_conta_origem).saldo_disponivel
    saldo_destino = service.conta_repo.get_saldo(
        id_conta_destino).saldo_disponivel

    assert saldo_origem == Decimal("200.00")
    assert saldo_destino == Decimal("50.00")


def test_pix_insufficient_funds(db_session, id_conta_origem, id_conta_destino):
    service = PixService(db_session)

    with pytest.raises(SaldoInsuficienteException):
        service.realizar_pix(id_conta_origem, id_conta_destino, 1000.00)

    saldo_origem = service.conta_repo.get_saldo(
        id_conta_origem).saldo_disponivel
    saldo_destino = service.conta_repo.get_saldo(
        id_conta_destino).saldo_disponivel

    assert saldo_origem == Decimal("0.00")
    assert saldo_destino == Decimal("0.00")
