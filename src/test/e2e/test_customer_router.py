import pytest


@pytest.mark.e2e
def test_create_customer_success(client):
    payload = {
        "nome": "Cliente Teste 100%",
        "cpf": "123.456.789-20",
        "sexo": "M",
        "email": "teste100@email.com",
        "senha": "senha145",
        "data_nascimento": "1995-01-01"
    }

    response = client.post("/api/v1/customer/", json=payload)
    print(response.json())
    assert response.status_code in [200, 201]


def test_searching_nonexistent_customer_account_return_404(client):
    response = client.get("/api/v1/customer/999999")
    assert response.status_code == 404
