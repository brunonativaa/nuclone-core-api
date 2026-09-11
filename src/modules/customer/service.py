from src.modules.customer.repository import ClienteRepository
from src.modules.customer.schema import ClienteCreateInput


class ClienteJaExisteException(Exception):
    pass


class ClienteNaoEncontradoException(Exception):
    pass


class ClienteService:

    def __init__(self, db):
        self.db = db
        self.customer_repo = ClienteRepository(db)

    def create_customer(self, data_customer: ClienteCreateInput | dict):
        # 1. Normalização do payload para o DTO do Pydantic
        if isinstance(data_customer, dict):
            customer_dto = ClienteCreateInput(**data_customer)
        else:
            customer_dto = data_customer

        # 2. Conversão para dicionário limpo para persistência
        customer_dict = customer_dto.model_dump()

        # 3. Tratamento de campos específicos (CPF higienizado)
        cpf_limpo = str(customer_dict["cpf"]).replace(
            ".", "").replace("-", "").strip()
        customer_dict["cpf"] = cpf_limpo

        # 4. Regra de Negócio: Unicidade de CPF
        customer_exist = self.customer_repo.get_by_cpf(cpf_limpo)
        if customer_exist:
            raise ClienteJaExisteException(
                "Já existe um cliente cadastrado com esse CPF."
            )

        # 5. Persistência Atômica
        try:
            new_customer = self.customer_repo.create(customer_dict)
            self.db.commit()
            return new_customer
        except Exception as e:
            self.db.rollback()
            raise e

    def get_by_id(self, id_cliente: int):
        customer = self.customer_repo.get_by_id(id_cliente)
        if not customer:
            raise ClienteNaoEncontradoException("Cliente não encontrado.")
        return customer

    def get_all(self):
        return self.customer_repo.get_all()
