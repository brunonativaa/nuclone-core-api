import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.core.database import get_db

cliente = TestClient(app)


@pytest.mark.e2e
def test_endpoint_realizar_pix_sem_autenticacao(db_session, id_conta_origem, id_conta_destino):
    # Força o FastAPI a usar a mesma sessão com SAVEPOINT criada na sua fixture
    def override_get_db():
        try:
            yield db_session
        finally:
            pass  # O fechamento já é controlado pela fixture db_session

    app.dependency_overrides[get_db] = override_get_db

    # Executa a requisição
    response = cliente.post(
        "/pix/v1/transferir",
        json={
            "id_conta_origem": id_conta_origem,
            "id_conta_destino": id_conta_destino,
            "valor": 10.50
        }
    )

    # Limpa as sobreposições após o teste rodar
    app.dependency_overrides.clear()

    # Agora a API vai encontrar as contas e retornar 200
    assert response.status_code == 200


cliente = TestClient(app)


@pytest.mark.e2e
def test_endpoint_realizar_pix_sem_autenticacao(db_session, id_conta_origem, id_conta_destino):
    # Força o FastAPI a usar a mesma sessão com SAVEPOINT criada na sua fixture
    def override_get_db():
        try:
            yield db_session
        finally:
            pass  # O fechamento já é controlado pela fixture db_session

    app.dependency_overrides[get_db] = override_get_db

    # Executa a requisição
    response = cliente.post(
        "/pix/v1/transferir",
        json={
            "id_conta_origem": id_conta_origem,
            "id_conta_destino": id_conta_destino,
            "valor": 10.50
        }
    )

    # Limpa as sobreposições após o teste rodar
    app.dependency_overrides.clear()

    # Agora a API vai encontrar as contas e retornar 200
    assert response.status_code == 200
