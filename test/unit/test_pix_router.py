from unittest.mock import MagicMock, patch
import pytest
from fastapi.testclient import TestClient

from src.main import app
from src.modules.pix.service import (
    ContaNaoEncontradaException,
    SaldoInsuficienteException,
)


client = TestClient(app)


# --- TESTES DA ROTA /transfer ---

@patch("src.modules.pix.router.PixService")
def test_transfer_pix_success(mock_pix_service):
    mock_service_instance = MagicMock()
    mock_pix_service.return_value = mock_service_instance

    mock_transaction = MagicMock()
    mock_transaction.id_transacao = 100
    mock_service_instance.make_pix_payment.return_value = mock_transaction

    payload = {"id_conta_origem": 1,
               "chave_destino": "teste@pix.com", "valor": 50.0}

    response = client.post("/api/v1/pix/transfer", json=payload)

    assert response.status_code == 200
    assert response.json()[
        "message"] == "Transferência PIX realizada com sucesso!"
    assert response.json()["id_transacao"] == 100


@patch("src.modules.pix.router.PixService")
def test_transfer_pix_conta_nao_encontrada(mock_pix_service):
    mock_service_instance = MagicMock()
    mock_pix_service.return_value = mock_service_instance
    mock_service_instance.make_pix_payment.side_effect = (
        ContaNaoEncontradaException("Conta de origem não encontrada.")
    )

    payload = {"id_conta_origem": 999,
               "chave_destino": "teste@pix.com", "valor": 50.0}

    response = client.post("/api/v1/pix/transfer", json=payload)

    assert response.status_code == 404
    assert response.json()["detail"] == "Conta de origem não encontrada."


@patch("src.modules.pix.router.PixService")
def test_transfer_pix_saldo_insuficiente(mock_pix_service):
    mock_service_instance = MagicMock()
    mock_pix_service.return_value = mock_service_instance
    mock_service_instance.make_pix_payment.side_effect = (
        SaldoInsuficienteException("Saldo insuficiente.")
    )

    payload = {"id_conta_origem": 1,
               "chave_destino": "teste@pix.com", "valor": 5000.0}

    response = client.post("/api/v1/pix/transfer", json=payload)

    assert response.status_code == 400
    assert response.json()["detail"] == "Saldo insuficiente."


@patch("src.modules.pix.router.PixService")
def test_transfer_pix_value_error(mock_pix_service):
    mock_service_instance = MagicMock()
    mock_pix_service.return_value = mock_service_instance
    mock_service_instance.make_pix_payment.side_effect = ValueError(
        "Valor inválido."
    )

    payload = {"id_conta_origem": 1,
               "chave_destino": "teste@pix.com", "valor": 10.0}

    response = client.post("/api/v1/pix/transfer", json=payload)

    assert response.status_code == 400
    assert response.json()["detail"] == "Valor inválido."

# --- TESTES DA ROTA /keys ---


@patch("src.modules.pix.router.PixService")
def test_create_pix_key_success(mock_pix_service):
    mock_service_instance = MagicMock()
    mock_pix_service.return_value = mock_service_instance

    mock_key = MagicMock()
    mock_key.id_chave = 10
    mock_key.valor_chave = "cliente@nuclone.com"
    mock_service_instance.register_pix_key.return_value = mock_key

    payload = {
        "id_conta": 1,
        "tipo_chave": "EMAIL",
        "valor_chave": "cliente@nuclone.com",
    }

    response = client.post("/api/v1/pix/keys", json=payload)

    assert response.status_code == 201
    assert response.json()["message"] == "Chave Pix Cadastrada com sucesso!"
    assert response.json()["id_chave"] == 10


@patch("src.modules.pix.router.PixService")
def test_create_pix_key_conta_nao_encontrada(mock_pix_service):
    mock_service_instance = MagicMock()
    mock_pix_service.return_value = mock_service_instance
    mock_service_instance.register_pix_key.side_effect = (
        ContaNaoEncontradaException("Conta não existe.")
    )

    payload = {
        "id_conta": 999,
        "tipo_chave": "EMAIL",
        "valor_chave": "cliente@nuclone.com",
    }

    response = client.post("/api/v1/pix/keys", json=payload)

    assert response.status_code == 404
    assert response.json()["detail"] == "Conta não existe."


@patch("src.modules.pix.router.PixService")
def test_create_pix_key_value_error(mock_pix_service):
    mock_service_instance = MagicMock()
    mock_pix_service.return_value = mock_service_instance
    mock_service_instance.register_pix_key.side_effect = ValueError(
        "Chave Pix já cadastrada."
    )

    payload = {
        "id_conta": 1,
        "tipo_chave": "EMAIL",
        "valor_chave": "repetida@nuclone.com",
    }

    response = client.post("/api/v1/pix/keys", json=payload)

    assert response.status_code == 400
    assert response.json()["detail"] == "Chave Pix já cadastrada."
