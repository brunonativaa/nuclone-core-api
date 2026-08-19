import pytest


def test_buscar_conta_por_id_sucesso(client, id_conta_origem):
    response = client.get(f"/api/v1/accounts/{id_conta_origem}/")
    print("RESPOSTA DA API", response.status_code, response.json())
    assert response.status_code == 200


def test_buscar_conta_inexistente_retorna_404(client):
    response = client.get("/api/v1/accounts/999999")
    assert response.status_code == 404
