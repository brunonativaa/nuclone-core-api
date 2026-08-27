import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.core.database import get_db

cliente = TestClient(app)


@pytest.fixture(autouse=True)
def override_db_dependency(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    yield
    app.dependency_overrides.clear()


@pytest.mark.e2e
def test_edpoint_execute_pix_success(id_conta_origem, id_conta_destino):
    response = cliente.post(
        "/api/v1/pix/transfer",
        json={
            "id_conta_origem": id_conta_origem,
            "id_conta_destino": id_conta_destino,
            "valor": 10.50
        }
    )
    assert response.status_code == 200


@pytest.mark.e2e
def test_endpoint_execute_pix_saldo_insuficiente_retorne_400(id_conta_origem, id_conta_destino):
    response = cliente.post(
        "/api/v1/pix/transfer",
        json={
            "id_conta_origem": id_conta_origem,
            "id_conta_destino": id_conta_destino,
            "valor": 999999.00

        }
    )
    assert response.status_code == 400


@pytest.mark.e2e
def test_endpoint_execut_pix_conta_inexistente_retorna_404(id_conta_origem):
    response = cliente.post(
        "/api/v1/pix/transfer",
        json={
            "id_conta_origem": id_conta_origem,
            "id_conta_destino": 999999,
            "valor": 10.50
        }
    )
    assert response.status_code == 404


@pytest.mark.e2e
def test_endpoint_execute_pix_mesma_conta_retorna_400(id_conta_origem):
    response = cliente.post(
        "/api/v1/pix/transfer",
        json={
            "id_conta_origem": id_conta_origem,
            "id_conta_destino": id_conta_origem,
            "valor": 10.50
        }
    )
    assert response.status_code == 400


@pytest.mark.e2e
def test_create_pix_key_success(id_conta_origem):
    payload = {
        "id_conta": id_conta_origem,
        "tipo_chave": "EMAIL"
    }
    response = cliente.post("/api/v1/pix/keys", json=payload)
    assert response.status_code in (200, 201)


@pytest.mark.e2e
def test_create_pix_key_conta_inexistente_retorna_404():
    payload = {
        "id_conta": 999999,
        "tipo_chave": "EMAIL"
    }
    response = cliente.post("/api/v1/pix/keys", json=payload)
    assert response.status_code == 404
