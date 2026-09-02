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

# Helper para extrair o ID numérico caso a fixture retorne a model Conta ou um int


def _get_id(conta_or_id) -> int:
    return getattr(conta_or_id, "id_conta", conta_or_id)


@pytest.mark.e2e
def test_edpoint_execute_pix_success(id_conta_origem, chave_pix_destino, client):
    response = client.post(
        "/api/v1/pix/transfer",
        json={
            "id_conta_origem": id_conta_origem,
            "chave_destino": chave_pix_destino,
            "valor": 10.50
        }
    )
    print(response.json())  # Exibirá a mensagem exata do detalhe do erro 404
    assert response.status_code == 200


@pytest.mark.e2e
def test_endpoint_execute_pix_saldo_insuficiente_retorne_400(id_conta_origem, chave_pix_destino, client):
    response = client.post(
        "/api/v1/pix/transfer",
        json={
            "id_conta_origem": id_conta_origem,
            "chave_destino": chave_pix_destino,
            "valor": 999999.00
        }
    )
    assert response.status_code == 400


@pytest.mark.e2e
def test_endpoint_execut_pix_conta_inexistente_retorna_404(id_conta_origem, client):
    response = client.post(
        "/api/v1/pix/transfer",
        json={
            "id_conta_origem": id_conta_origem,
            "chave_destino": "chave_inexistente@email.com",
            "valor": 10.50
        }
    )
    assert response.status_code == 404


@pytest.mark.e2e
def test_endpoint_execute_pix_mesma_conta_retorna_400(id_conta_origem, chave_pix_origem, client):
    response = client.post(
        "/api/v1/pix/transfer",
        json={
            "id_conta_origem": id_conta_origem,
            "chave_destino": chave_pix_origem,
            "valor": 10.50
        }
    )
    assert response.status_code == 400
