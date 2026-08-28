from faker import Faker
import pytest

fake = Faker('pt_BR')


@pytest.mark.e2e
def test_create_customer_success(client):
    payload = {
        "nome": fake.name(),
        "cpf": fake.cpf().replace(".", "").replace("-", ""),
        "sexo": "M",
        "email": fake.email(),
        "senha": "senha145",
        "data_nascimento": "2002-04-07"
    }

    response = client.post("/api/v1/customers", json=payload)
    print(response.json())
    assert response.status_code in [200, 201]


def test_searching_nonexistent_customer_account_return_404(client):
    response = client.get("/api/v1/customers/999999")
    assert response.status_code == 404
