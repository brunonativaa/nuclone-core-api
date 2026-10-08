from decimal import Decimal
import pytest

from src.modules.account.exceptions import (
    ClienteNaoEncontradoException,
    ContaNaoEncontradaException as AccountContaNaoEncontradaException,
)
from src.modules.account.service import ContaService
from src.modules.pix.exceptions import ContaNaoEncontradaException
from src.modules.pix.service import PixService, SaldoInsuficienteException


@pytest.mark.asyncio
async def test_perform_pix_nonexistent_source_account(db_session):
    service = PixService(db_session)
    nonexistent_account_id = 999999

    with pytest.raises(ContaNaoEncontradaException) as exc_info:
        await service.make_pix_payment(
            id_conta_origem=nonexistent_account_id,
            id_conta_destino=1,
            valor=Decimal("50.00"),
        )

    assert f"Conta com ID {nonexistent_account_id}" in str(exc_info.value)


@pytest.mark.asyncio
async def test_perform_pix_nonexistent_destination_account(db_session, id_conta_origem):
    service = PixService(db_session)
    nonexistent_account_id = 999999

    with pytest.raises(ContaNaoEncontradaException) as exc_info:
        await service.make_pix_payment(
            id_conta_origem=id_conta_origem,
            id_conta_destino=nonexistent_account_id,
            valor=Decimal("50.00"),
        )

    assert f"Conta com ID {nonexistent_account_id}" in str(exc_info.value)


@pytest.mark.asyncio
async def test_perform_pix_same_account(db_session, id_conta_origem):
    service = PixService(db_session)
    with pytest.raises(
        ValueError, match="Não é possível realizar transferência PIX para a mesma conta."
    ):
        await service.make_pix_payment(
            id_conta_origem=id_conta_origem,
            id_conta_destino=id_conta_origem,
            valor=Decimal("50.00"),
        )


@pytest.mark.asyncio
async def test_adding_balance_invalid_value(db_session, id_conta_origem):
    conta_service = ContaService(db_session)
    with pytest.raises(ValueError, match="O valor adicionado deve ser maior que zero."):
        await conta_service.credit(id_conta_origem, Decimal("-10.00"))


@pytest.mark.asyncio
async def test_adding_balance_nonexistent_account(db_session):
    conta_service = ContaService(db_session)
    nonexistent_account_id = 999999

    with pytest.raises(AccountContaNaoEncontradaException) as exc_info:
        await conta_service.credit(nonexistent_account_id, Decimal("100.00"))

    assert exc_info.value.id_conta == nonexistent_account_id
    assert f"Conta com ID {nonexistent_account_id} não encontrada." in str(exc_info.value)


@pytest.mark.asyncio
async def test_perform_pix_failure_bank_rollback(
    db_session, id_conta_origem, id_conta_destino, mocker
):
    service = PixService(db_session)
    conta_service = ContaService(db_session)
    await conta_service.credit(id_conta_origem, Decimal("250.00"))

    mocker.patch.object(
        service.pix_repo,
        "record_transaction",
        side_effect=Exception("Erro forçado do banco"),
    )

    with pytest.raises(Exception, match="Erro forçado do banco"):
        await service.make_pix_payment(
            id_conta_origem=id_conta_origem,
            id_conta_destino=id_conta_destino,
            valor=Decimal("50.00"),
        )


@pytest.mark.asyncio
async def test_adding_balance_to_account(db_session, id_conta_origem):
    conta_service = ContaService(db_session)

    conta_dto = await conta_service.get_balance(id_conta_origem)
    saldo_inicial = conta_dto.saldo_disponivel
    await conta_service.credit(id_conta_origem, Decimal("250.00"))

    conta_dto_final = await conta_service.get_balance(id_conta_origem)
    saldo_final = conta_dto_final.saldo_disponivel
    assert saldo_final == saldo_inicial + Decimal("250.00")


@pytest.mark.asyncio
async def test_successfully_complete_a_pix_transfer(
    db_session, id_conta_origem, id_conta_destino
):
    service = PixService(db_session)
    conta_service = ContaService(db_session)

    conta_dto = await conta_service.get_balance(id_conta_origem)
    saldo_inicial_origem = conta_dto.saldo_disponivel

    await conta_service.credit(id_conta_origem, Decimal("250.00"))

    transacao = await service.make_pix_payment(
        id_conta_origem=id_conta_origem,
        id_conta_destino=id_conta_destino,
        valor=Decimal("50.00"),
    )

    assert transacao.valor == Decimal("50.00")

    conta_dto_origem = await conta_service.get_balance(id_conta_origem)
    saldo_origem = conta_dto_origem.saldo_disponivel

    conta_dto_destino = await conta_service.get_balance(id_conta_destino)
    saldo_destino = conta_dto_destino.saldo_disponivel

    assert saldo_origem == saldo_inicial_origem + Decimal("200.00")
    assert saldo_destino == Decimal("50.00")


@pytest.mark.asyncio
async def test_pix_insufficient_funds(db_session, id_conta_origem, id_conta_destino):
    service = PixService(db_session)
    conta_service = ContaService(db_session)

    conta_dto = await conta_service.get_balance(id_conta_origem)
    saldo_inicial_origem = conta_dto.saldo_disponivel

    with pytest.raises(SaldoInsuficienteException):
        await service.make_pix_payment(
            id_conta_origem=id_conta_origem,
            id_conta_destino=id_conta_destino,
            valor=Decimal("1000.00"),
        )

    conta_dto_final = await conta_service.get_balance(id_conta_origem)
    saldo_origem_final = conta_dto_final.saldo_disponivel

    assert saldo_origem_final == saldo_inicial_origem