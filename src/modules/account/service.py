import random
from pydantic import BaseModel
from src.modules.account.model import ContaModel
from src.modules.account.repository import ContaRepository
from src.modules.account.schema import AccountCreateInput
from src.modules.customer.repository import ClienteRepository


class ContaNaoEncontradaException(Exception):
    pass


class ClienteNaoEncontradoException(Exception):
    pass


class ContaService:

    def __init__(self, db):
        self.db = db
        self.conta_repo = ContaRepository(db)
        self.cliente_repo = ClienteRepository(db)

    def _gerar_num_conta(self) -> str:
        return str(random.randint(100000, 999999))

    def create_account(self, data_conta) -> ContaModel:
        # Conversão polimórfica: aceita Pydantic DTO ou dict
        payload = (
            data_conta.model_dump()
            if isinstance(data_conta, BaseModel)
            else data_conta.copy()
        )

        id_cliente = payload.get("id_cliente")

        # 1. Validação da Regra de Negócio
        cliente = self.cliente_repo.get_by_id(id_cliente)
        if not cliente:
            raise ClienteNaoEncontradoException("Cliente não encontrado.")

        # 2. Regras de preenchimento
        if not payload.get("num_conta"):
            payload["num_conta"] = self._gerar_num_conta()

        if not payload.get("agencia"):
            payload["agencia"] = "0001"

        try:
            # 3. Transação Atômica
            nova_conta = self.conta_repo.create_account(payload)
            self.conta_repo.create_saldo(nova_conta.id_conta)

            self.db.commit()
            return nova_conta
        except Exception as e:
            self.db.rollback()
            raise e

    def get_by_id(self, id_conta: int) -> ContaModel:
        account = self.conta_repo.search_account(id_conta)
        if not account:
            raise ContaNaoEncontradaException(
                f"Conta com ID {id_conta} não encontrada."
            )
        return account

    def get_saldo(self, id_conta: int):
        conta = self.conta_repo.search_account(id_conta)
        if not conta:
            raise ContaNaoEncontradaException("Conta não encontrada.")
        return self.conta_repo.get_saldo(id_conta)
