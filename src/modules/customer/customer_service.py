from src.modules.customer.customer_repository import ClienteRepository


class ClienteJaExisteException(Exception):
    pass


class ClienteNaoEncontradoException(Exception):
    pass


class ClienteService:

    def __init__(self, db):
        self.db = db
        self.customer_repo = ClienteRepository(db)

    def create_customer(self, data_customer: dict):

        required_fields = ["nome", "cpf", "email"]
        for field in required_fields:
            if field not in data_customer or not data_customer[field]:
                raise ValueError(f"O field '{field}' é obrigatório.")

        if "cpf" in data_customer and data_customer["cpf"]:
            cpf_clear = str(data_customer["cpf"]).replace(
                ".", "").replace("-", "").strip()
            data_customer["cpf"] = cpf_clear

        customer_exist = self.customer_repo.get_by_cpf(cpf_clear)
        if customer_exist:
            raise ClienteJaExisteException(
                "Já existe um cliente cadastrado com esse cpf.")

        try:
            new_customer = self.customer_repo.create(data_customer)
            self.db.commit()
            return new_customer
        except Exception as e:
            self.db.rollback()
            raise e

    def get_by_id(self, id_cliente: int):
        customer = self.customer_repo.get_by_id(id_cliente)

        if not customer:
            raise ClienteNaoEncontradoException("Cliente não encontrado")

        return customer

    def get_all(self):
        return self.customer_repo.get_all()
