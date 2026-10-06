from typing import Union
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.security import hash_password
from src.modules.customer.model import ClienteModel
from src.modules.customer.repository import ClienteRepository
from src.modules.customer.schema import ClienteCreateInput


class ClienteJaExisteException(Exception):
    pass


class ClienteNaoEncontradoException(Exception):
    pass


class ClienteService:

    def __init__(self, db: AsyncSession):
        self.db = db
        self.customer_repo = ClienteRepository(db)

    async def create_customer(self, data_customer: Union[ClienteCreateInput, dict]) -> ClienteModel:
    
        cliente_dict = (
            data_customer.model_dump()
            if isinstance(data_customer, BaseModel)
            else data_customer.copy()
        )

        # 2. Higienização do CPF
        cpf_limpo = (
            str(cliente_dict["cpf"])
            .replace(".", "")
            .replace("-", "")
            .strip()
        )
        cliente_dict["cpf"] = cpf_limpo

        # 3. Regra de Negócio: Unicidade de CPF
        cliente_existente = await self.customer_repo.get_by_cpf(cpf_limpo)
        if cliente_existente:
            raise ClienteJaExisteException(
                "Já existe um cliente cadastrado com esse CPF."
            )

        # 4. Extração Segura e Criptografia das Credenciais
        raw_password = cliente_dict.pop(
            "senha_hash", None) or cliente_dict.pop("senha", None)
        raw_pin = cliente_dict.pop("pin_transacao_hash", None) or cliente_dict.pop(
            "pin_transacao", None) or cliente_dict.pop("pin", None)

        if not raw_password or not raw_pin:
            raise ValueError(
                "Senha e PIN de transação são obrigatórios para o cadastro.")

        # 5. Criptografia dos Segredos
        cliente_dict["senha_hash"] = hash_password(str(raw_password))
        cliente_dict["pin_transacao_hash"] = hash_password(str(raw_pin))

        # 6. Persistência Atômica
        try:
            novo_cliente = await self.customer_repo.create(cliente_dict)
            await self.db.commit()
            await self.db.refresh(novo_cliente)
            return novo_cliente
        except Exception as e:
            await self.db.rollback()
            raise e

    async def get_by_id(self, id_cliente: int ) -> ClienteModel:
        cliente = await self.customer_repo.get_by_id(id_cliente)
        if not cliente:
            raise ClienteNaoEncontradoException(f"Cliente {id_cliente} não encontrado.")
        return cliente

