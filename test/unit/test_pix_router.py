from unittest.mock import AsyncMock, patch
import pytest
from fastapi import status

from src.modules.pix.exceptions import (
    ContaNaoEncontradaException,
    SaldoInsuficienteException,
    ChavePixDuplicadaException,
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

    payload = {
        "id_conta_origem": 1,
        "chave_destino": "teste@pix.com",
        "valor": 50.0,
    }

    response = await client.post("/api/v1/pix/transfer", json=payload)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == "Transferência PIX realizada com sucesso!"
    assert response.json()["id_transacao"] == 100


@pytest.mark.asyncio
@patch("src.modules.pix.router.PixService")
async def test_transfer_pix_account_not_found(mock_pix_service, client):
    mock_service_instance = AsyncMock()
    mock_pix_service.return_value = mock_service_instance
    
    # ✅ Passa o ID numérico 999 exigido pela exceção
    mock_service_instance.make_pix_payment.side_effect = ContaNaoEncontradaException(999)

    payload = {
        "id_conta_origem": 999,
        "chave_destino": "teste@pix.com",
        "valor": 50.0,
    }

    response = await client.post("/api/v1/pix/transfer", json=payload)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Conta com ID 999 não encontrada para a transação PIX."


@pytest.mark.asyncio
@patch("src.modules.pix.router.PixService")
async def test_transfer_pix_insufficient_balance(mock_pix_service, client):
    mock_service_instance = AsyncMock()
    mock_pix_service.return_value = mock_service_instance
    
    # ✅ Instanciação sem argumentos gera a mensagem padrão limpa
    mock_service_instance.make_pix_payment.side_effect = SaldoInsuficienteException()

    payload = {
        "id_conta_origem": 1,
        "chave_destino": "teste@pix.com",
        "valor": 5000.0,
    }

    response = await client.post("/api/v1/pix/transfer", json=payload)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Saldo insuficiente para realizar a transferência PIX."


@pytest.mark.asyncio
@patch("src.modules.pix.router.PixService")
async def test_transfer_pix_value_error(mock_pix_service, client):
    mock_service_instance = AsyncMock()
    mock_pix_service.return_value = mock_service_instance
    mock_service_instance.make_pix_payment.side_effect = ValueError("Valor inválido.")

    payload = {
        "id_conta_origem": 1,
        "chave_destino": "teste@pix.com",
        "valor": 10.0,
    }

    response = await client.post("/api/v1/pix/transfer", json=payload)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Valor inválido."


# --- TESTES DA ROTA /keys ---

@pytest.mark.asyncio
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

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["message"] == "Chave Pix Cadastrada com sucesso!"
    assert response.json()["id_chave"] == 10


@pytest.mark.asyncio
@patch("src.modules.pix.router.PixService")
async def test_create_pix_key_account_not_found(mock_pix_service, client):
    mock_service_instance = AsyncMock()
    mock_pix_service.return_value = mock_service_instance

    # ✅ Passa o ID numérico 999
    mock_service_instance.register_pix_key.side_effect = ContaNaoEncontradaException(999)

    payload = {
        "id_conta": 999,
        "tipo_chave": "EMAIL",
        "valor_chave": "cliente@nuclone.com",
    }

    response = await client.post("/api/v1/pix/keys", json=payload)

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
@patch("src.modules.pix.router.PixService")
async def test_create_pix_key_value_error(mock_pix_service, client):
    mock_service_instance = AsyncMock()
    mock_pix_service.return_value = mock_service_instance

    # ✅ Passa o valor da chave cadastrada
    mock_service_instance.register_pix_key.side_effect = ChavePixDuplicadaException(
        "repetida@nuclone.com"
    )

    payload = {
        "id_conta": 1,
        "tipo_chave": "EMAIL",
        "valor_chave": "repetida@nuclone.com",
    }

    response = await client.post("/api/v1/pix/keys", json=payload)

    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json()["detail"] == "A chave PIX 'repetida@nuclone.com' já está cadastrada no sistema."