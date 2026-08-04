import random
from src.repositories.conta_repository import ContaRepository
from src.repositories.cliente_repository import ClienteRepository


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
        # Gera um número de conta aleatório de 6 dígitos
        return str(random.randint(100000, 999999))

    def create_account(self, data_conta: dict):
        id_cliente = data_conta.get("id_cliente")

        # 1. Regra de Negócio: O cliente precisa existir
        cliente = self.cliente_repo.get_by_id(id_cliente)
        if not cliente:
            raise ClienteNaoEncontradoException("Cliente não encontrado.")

        # 2. Se não veio num_conta, gera automaticamente
        if "num_conta" not in data_conta or not data_conta["num_conta"]:
            data_conta["num_conta"] = self._gerar_num_conta()

        if "agencia" not in data_conta:
            data_conta["agencia"] = "0001"

        try:
            # 3. Cria a conta
            nova_conta = self.conta_repo.create_account(data_conta)

            # 4. Cria o registro de saldo zerado atrelado a essa conta
            self.conta_repo.create_saldo(nova_conta.id_conta)

            # Commit único da transação inteira
            self.db.commit()
            return nova_conta
        except Exception as e:
            self.db.rollback()
            raise e

    def get_saldo(self, id_conta: int):
        conta = self.conta_repo.search_account(id_conta)
        if not conta:
            raise ContaNaoEncontradaException("Conta não encontrada.")

        saldo = self.conta_repo.get_saldo(id_conta)
        return saldo
