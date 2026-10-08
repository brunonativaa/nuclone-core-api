from unittest.mock import AsyncMock, MagicMock, patch
import pytest
from fastapi import status

from src.main import app
from src.modules.pix.service import (
    ContaNaoEncontradaException,
    SaldoInsuficienteException,
    ChavePixDuplicadaException
)



# --- TESTES DA ROTA /transfer ---
@pytest.mark.asyncio
@patch("src.modules.pix.router.PixService")
async def test_transfer_pix_success(mock_pix_service, client):
    mock_service_instance = AsyncMock()
    mock_pix_service.return_value = mock_service_instance

    mock_transaction = AsyncMock()
    mock_transaction.id_transacao = 100
    mock_service_instance.make_pix_payment.return_value = mock_transaction

    payload = {"id_conta_origem": 1,
               "chave_destino": "teste@pix.com", "valor": 50.0}

    response = await client.post("/api/v1/pix/transfer", json=payload)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()[
        "message"] == "Transferência PIX realizada com sucesso!"
    assert response.json()["id_transacao"] == 100

@pytest.mark.asyncio
@patch("src.modules.pix.router.PixService")
async def test_transfer_pix_account_not_found(mock_pix_service, client):
    mock_service_instance = AsyncMock()
    mock_pix_service.return_value = mock_service_instance
    mock_service_instance.make_pix_payment.side_effect = (
        ContaNaoEncontradaException("Conta de origem não encontrada.")
    )

    payload = {"id_conta_origem": 999,
               "chave_destino": "teste@pix.com", "valor": 50.0}

    response = await client.post("/api/v1/pix/transfer", json=payload)

    assert response.status_code == 404
    assert response.json()["detail"] == "Conta de origem não encontrada."

@pytest.mark.asyncio
@patch("src.modules.pix.router.PixService")
async def test_transfer_pix_insufficient_balance(mock_pix_service, client):
    mock_service_instance = AsyncMock()
    mock_pix_service.return_value = mock_service_instance
    mock_service_instance.make_pix_payment.side_effect = (
        SaldoInsuficienteException("Saldo insuficiente.")
    )

    payload = {"id_conta_origem": 1,
               "chave_destino": "teste@pix.com", "valor": 5000.0}

    response = await client.post("/api/v1/pix/transfer", json=payload)

    assert response.status_code == 400
    assert response.json()["detail"] == "Saldo insuficiente."

@pytest.mark.asyncio
@patch("src.modules.pix.router.PixService")
async def test_transfer_pix_value_error(mock_pix_service, client):
    mock_service_instance = AsyncMock()
    mock_pix_service.return_value = mock_service_instance
    mock_service_instance.make_pix_payment.side_effect = ValueError(
        "Valor inválido."
    )

    payload = {"id_conta_origem": 1,
               "chave_destino": "teste@pix.com", "valor": 10.0}

    response = await client.post("/api/v1/pix/transfer", json=payload)

    assert response.status_code == 400
    assert response.json()["detail"] == "Valor inválido."

# --- TESTES DA ROTA /keys ---


@patch("src.modules.pix.router.PixService")
async def test_create_pix_key_success(mock_pix_service, client):
    mock_service_instance = AsyncMock()
    mock_pix_service.return_value = mock_service_instance

    mock_key = AsyncMock()
    mock_key.id_chave = 10
    mock_key.valor_chave = "cliente@nuclone.com"
    mock_service_instance.register_pix_key.return_value = mock_key

    payload = {
        "id_conta": 1,
        "tipo_chave": "EMAIL",
        "valor_chave": "cliente@nuclone.com",
    }

    response = await client.post("/api/v1/pix/keys", json=payload)

    assert response.status_code == 201
    assert response.json()["message"] == "Chave Pix Cadastrada com sucesso!"
    assert response.json()["id_chave"] == 10


@patch("src.modules.pix.router.PixService")
async def test_create_pix_key_account_not_found(mock_pix_service, client):
    mock_service_instance = AsyncMock()
    mock_pix_service.return_value = mock_service_instance

    mock_service_instance.register_pix_key.side_effect = (
        ContaNaoEncontradaException("Conta não existe.")
    )

    payload = {
        "id_conta": 999,
        "tipo_chave": "EMAIL",
        "valor_chave": "cliente@nuclone.com",
    }

    response = await client.post("/api/v1/pix/keys", json=payload)

    assert response.status_code == 404



@patch("src.modules.pix.router.PixService")
async def test_create_pix_key_value_error(mock_pix_service, client):
    mock_service_instance = AsyncMock()
    mock_pix_service.return_value = mock_service_instance
    mock_service_instance.register_pix_key.side_effect = ChavePixDuplicadaException(
        "Chave Pix já cadastrada."
    )

    payload = {
        "id_conta": 1,
        "tipo_chave": "EMAIL",
        "valor_chave": "repetida@nuclone.com",
    }

    response = await client.post("/api/v1/pix/keys", json=payload)

    assert response.status_code == 409
    assert response.json()["detail"] == "Chave Pix já cadastrada."
