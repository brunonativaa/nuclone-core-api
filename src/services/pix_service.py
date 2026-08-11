from decimal import Decimal
from src.models.transaction_model import TipoTransacaoEnum
from src.repositories.account_repository import ContaRepository
from src.repositories.pix_repository import PixRepository


class SaldoInsuficienteException(Exception):
    pass


class ContaNaoEncontradaException(Exception):
    pass


class PixService:

    def __init__(self, db):
        self.db = db
        self.conta_repo = ContaRepository(db)
        self.pix_repo = PixRepository(db)

    def realizar_pix(self, id_conta_origem: int, id_conta_destino: int, valor):

        valor_decimal = Decimal(str(valor))

        conta_origem = self.conta_repo.search_account(id_conta_origem)
        conta_destino = self.conta_repo.search_account(id_conta_destino)

        if not conta_origem:
            raise ContaNaoEncontradaException(
                "Conta de origem não encontrada.")

        if not conta_destino:
            raise ContaNaoEncontradaException(
                "Conta de destino não encontrada.")

        if id_conta_origem == id_conta_destino:
            raise ValueError(
                "Não é possivel realizar Pix para a própria conta.")

        saldo_origem = self.conta_repo.get_saldo(id_conta_origem)

        if saldo_origem.saldo_disponivel < valor_decimal:
            raise SaldoInsuficienteException(
                "Saldo insuficiente para realizar o Pix")

        try:

            self.pix_repo.debit(id_conta_origem, valor_decimal)

            self.pix_repo.credit(id_conta_destino, valor_decimal)

            dados_transacao = self.pix_repo.record_transaction({
                "id_conta_origem": id_conta_origem,
                "id_conta_destino": id_conta_destino,
                "tipo_transacao": TipoTransacaoEnum.PIX,
                "valor": valor_decimal



            })

            self.db.flush()
            self.db.commit()
            return dados_transacao

        except Exception as e:

            self.db.rollback()
            raise e

    def adding_balance(self, id_conta: int, valor):
        valor_decimal = Decimal(str(valor))

        if valor_decimal <= 0:
            raise ValueError("O valor adicionado deve ser maior que zero.")

        conta = self.conta_repo.search_account(id_conta)
        if not conta:
            raise ContaNaoEncontradaException("Conta não encontrada.")

        try:

            saldo_atualizado = self.pix_repo.credit(id_conta, valor_decimal)

            self.db.commit()
            return saldo_atualizado

        except Exception as e:
            self.db.rollback()
            return e
