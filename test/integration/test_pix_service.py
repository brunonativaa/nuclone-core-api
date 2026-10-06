import pytest
from decimal import Decimal
from src.modules.pix.service import (
    PixService,
    SaldoInsuficienteException,
    ContaNaoEncontradaException
)
from src.modules.account.service import ContaService

@pytest.mark.asyncio
async def test_perform_pix_nonexistent_source_account(db_session, id_conta_destino):
    service = PixService(db_session)
    with pytest.raises(ContaNaoEncontradaException, match="Conta de origem não encontrada."):
        await service.make_pix_payment(999999, id_conta_destino, Decimal("50.00"))


@pytest.mark.asyncio
async def test_perform_pix_nonexistent_destination_account(db_session, id_conta_origem):
    service = PixService(db_session)
    with pytest.raises(ContaNaoEncontradaException, match="Conta de destino não encontrada"):
        await service.make_pix_payment(id_conta_origem, 999999, Decimal("50.00"))

@pytest.mark.asyncio
async def test_perform_pix_same_account(db_session, id_conta_origem):
    service = PixService(db_session)
    with pytest.raises(ValueError, match="Não é possível realizar transferência PIX para a mesma conta."):
        await service.make_pix_payment(
            id_conta_origem, id_conta_origem, Decimal("50.00"))


@pytest.mark.asyncio
async def test_adding_balance_invalid_value(db_session, id_conta_origem):
    service = PixService(db_session)
    with pytest.raises(ValueError, match="O valor adicionado deve ser maior que zero."):
        await service.adding_balance(id_conta_origem, Decimal("-10.00"))


@pytest.mark.asyncio
async def test_adding_balance_nonexistent_account(db_session):
    service = PixService(db_session)
    with pytest.raises(ContaNaoEncontradaException, match="Conta não encontrada."):
        await service.adding_balance(999999, Decimal("100.00"))


@pytest.mark.asyncio
async def test_perform_pix_failure_bank_rollback(db_session, id_conta_origem, id_conta_destino, mocker):
    service = PixService(db_session)
    await service.adding_balance(id_conta_origem, 250.00)

    mocker.patch.object(service.pix_repo, "record_transaction",
                        side_effect=Exception("Erro forçado do banco"))

    with pytest.raises(Exception, match="Erro forçado do banco"):
        await service.make_pix_payment(
            id_conta_origem, id_conta_destino, Decimal("50.00"))

# Validates the account deposit transaction

@pytest.mark.asyncio
async def test_adding_balance_to_account(db_session, id_conta_origem):
    service = PixService(db_session)
    conta_service = ContaService(db_session)

    conta_dto = await conta_service.get_balance(id_conta_origem)
    saldo_inicial = conta_dto.saldo_disponivel
    await service.adding_balance(id_conta_origem, 250.00)

    conta_dto_final = await conta_service.get_balance(id_conta_origem)
    saldo_final = conta_dto_final.saldo_disponivel
    assert saldo_final == saldo_inicial + Decimal("250.00")

@pytest.mark.asyncio
async def test_successfully_complete_a_pix_transfer(db_session, id_conta_origem, id_conta_destino):
    service = PixService(db_session)
    conta_service = ContaService(db_session)

    conta_dto = await conta_service.get_balance(id_conta_origem)
    saldo_inicial_origem = conta_dto.saldo_disponivel

    await service.adding_balance(id_conta_origem, Decimal("250.00"))

    transacao = await service.make_pix_payment(
        id_conta_origem, id_conta_destino, Decimal("50.00"))

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


    conta_dto =await conta_service.get_balance(id_conta_origem)
    saldo_inicial_origem = conta_dto.saldo_disponivel

    with pytest.raises(SaldoInsuficienteException):
        await service.make_pix_payment(id_conta_origem, id_conta_destino, Decimal("1000.00"))

        conta_dto_final = await conta_service.get_balance(id_conta_origem)
        saldo_origem_final = conta_dto_final.saldo_disponivel

        assert saldo_origem_final == saldo_inicial_origem
