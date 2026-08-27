import pytest


def test_find_account_by_id_success(client, id_conta_origem):
    response = client.get(f"/api/v1/accounts/{id_conta_origem}/")
    print("RESPOSTA DA API", response.status_code, response.json())
    assert response.status_code == 200


def test_retrieve_nonexistent_account_returns_404(client):
    response = client.get("/api/v1/accounts/999999")
    assert response.status_code == 404


def test_search_account_invalid_id_return_422(client):
    response = client.get("/api/v1/accounts/abc")
    assert response.status_code == 422
