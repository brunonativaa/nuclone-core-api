from datetime import datetime
from decimal import Decimal
from src.repositories.conta_repository import ContaRepository
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

        conta_origem = self.conta_repo.buscar_conta(id_conta_origem)
        conta_destino = self.conta_repo.buscar_conta(id_conta_destino)


        if not conta_origem:
            raise ContaNaoEncontradaException("Conta de origem não encontrada.")

        if not conta_destino:
            raise ContaNaoEncontradaException("Conta de destino não encontrada.")

        saldo_origem = self.conta_repo.get_saldo(id_conta_origem)

        if saldo_origem.saldo_disponivel < valor_decimal:
            raise SaldoInsuficienteException("Saldo insuficiente para realizar o Pix")

        self.pix_repo.debitar(id_conta_origem, valor_decimal)

        self.pix_repo.creditar(id_conta_destino, valor_decimal)

        dados_transacao = self.registrar_transacao ({
            "id_conta_origem": id_conta_origem,
            "id_conta_destino": id_conta_destino,
            "valor": valor_decimal,
            "tipo": "PIX"
            
        })

        return dados_transacao