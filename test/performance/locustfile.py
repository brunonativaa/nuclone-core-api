import random
from locust import HttpUser, task, between


class NucloneUser(HttpUser):

    wait_time = between(1, 3)

    def on_start(self):
        # Garante exatamente 11 dígitos numéricos para o CPF
        cpf_gerado = str(random.randint(1000000000, 99999999999)).zfill(11)

        res_customer = self.client.post(
            "/api/v1/customers",
            json={
                "nome": "Cliente Locust",
                "cpf": cpf_gerado,
                "sexo": "M",
                "email": f"locust_{cpf_gerado}@nuclone.com",
                "senha": "hash_senha_teste",
                "data_nascimento": "1995-08-15",
            },
        )

        if res_customer.status_code in (200, 201):
            self.id_cliente = res_customer.json().get("id_cliente")

        if res_customer.status_code == 201:
            self.id_cliente = res_customer.json().get("id_cliente")

    @task(3)
    def get_account_by_id(self):
        id_conta = getattr(self, "id_conta", 3)
        self.client.get(f"/api/v1/accounts/{id_conta}")

    @task
    def realizar_transferencia_pix(self):
        payload = {
            "id_conta_origem": 3,
            "chave_destino": "mariana@nuclone.com",
            "valor": 1.00
        }

        self.client.post("/api/v1/pix/transfer", json=payload)
