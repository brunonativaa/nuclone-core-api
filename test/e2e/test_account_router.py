import pytest


def test_create_account_client_not_found_raises_404(client):
    payload = {
        "id_cliente": 999999,  # Id not exist
        "limite": 1000.00
    }

    response = client.post("/api/v1/accounts", json=payload)

    assert response.status_code == 404
    assert response.json()["detail"]["code"] == "CLIENT_NOT_FOUND"


def test_get_account_by_id_not_found_raises_404(client):
    response = client.get("/api/v1/accounts/999999")

    assert response.status_code == 404
    assert response.json()[
        "detail"]["message"] == "Conta 999999 não encontrada"


def test_get_account_balance_not_found_raises_404(client):
    response = client.get("/api/v1/accounts/999999/balance")

    assert response.status_code == 404
    assert response.json()["detail"]["error"] == "Conta Não Encontrada"


def test_find_account_by_id_success(client, id_conta_origem):
    response = client.get(f"/api/v1/accounts/{id_conta_origem}")
    print("RESPOSTA DA API", response.status_code, response.json())
    assert response.status_code == 200


def test_retrieve_nonexistent_account_returns_404(client):
    response = client.get("/api/v1/accounts/999999")
    assert response.status_code == 404


def test_search_account_invalid_id_return_422(client):
    response = client.get("/api/v1/accounts/abc")
    assert response.status_code == 422
