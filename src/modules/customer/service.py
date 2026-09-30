from src.core.security import hash_password
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
        # 1. Garantia de Tipagem via DTO
        if isinstance(data_customer, dict):
            customer_dto = ClienteCreateInput(**data_customer)
        else:
            customer_dto = data_customer

        # Converte para dicionário
        customer_dict = customer_dto.model_dump()

        # 2. Higienização do CPF
        cpf_limpo = str(customer_dict["cpf"]).replace(
            ".", "").replace("-", "").strip()
        customer_dict["cpf"] = cpf_limpo

        # 3. Regra de Negócio: Unicidade de CPF
        customer_exist = self.customer_repo.get_by_cpf(cpf_limpo)
        if customer_exist:
            raise ClienteJaExisteException(
                "Já existe um cliente cadastrado com esse CPF."
            )

        # 4. Extração Segura com Tratamento para Nomes Correto de Campos
        # Suporta tanto o campo com o nome da entidade quanto a versão em texto plano do DTO
        raw_password = customer_dict.pop(
            "senha_hash", None) or customer_dict.pop("senha", None)
        raw_pin = customer_dict.pop("pin_transacao_hash", None) or customer_dict.pop(
            "pin_transacao", None) or customer_dict.pop("pin", None)

        if not raw_password or not raw_pin:
            raise ValueError(
                "Senha e PIN de transação são obrigatórios para o cadastro.")

        # 5. Criptografia dos Segredos
        customer_dict["senha_hash"] = hash_password(raw_password)
        customer_dict["pin_transacao_hash"] = hash_password(raw_pin)

        # 6. Persistência Atômica
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
