from locust import HttpUser, task, between

class NucloneUser(HttpUser):
    # Tempo de espera entre uma requisição e outra (em segundos)
    wait_time = between(1, 3)
    
    @task(1)
    def testar_health_check(self):
        """Simula requisições à rota pública"""
        self.client.get("/")

    def on_start(self):
        """Executado quando um usuário virtual é iniciado: faz o login para pegar o token"""
        response = self.client.post("/api/v1/auth/login", data={
            "username": "1225825501",
            "password": "lucas123"
        })
        if response.status_code == 200:
            self.token = response.json().get("access_token")
            self.headers = {"Authorization": f"Bearer {self.token}"}
        else:
            self.token = None
            self.headers = {}

    @task(3)
    def testar_extrato(self):
        """Simula usuários consultando o extrato (peso 3: acontece mais vezes)"""
        if self.token:
            self.client.get("/api/v1/extrato", headers=self.headers)

   