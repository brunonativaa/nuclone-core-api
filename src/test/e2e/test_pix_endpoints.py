import pytest
from fastapi.testclient import TestClient
from src.main import app


cliente = TestClient(app)


@pytest.mark.e2e
def test_endpoint_realizar_pix_sem_autenticacao():
    response = cliente.post("/pix/v1/transferir", json={
        "id_conta_origem": 1,
        "id_conta_destino": 2,
        "valor": 0.00
    })

    assert response.status_code == 200
