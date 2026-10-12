
from src.core.exceptions import DomainException

class ContaNaoEncontradaException(DomainException):
    def __init__(self, id_conta: int):
        self.id_conta = id_conta
        super().__init__(f"Conta com ID {id_conta} não encontrada.")

class ClienteNaoEncontradoException(DomainException):
    def __init__(self, id_cliente: int):
        self.id_cliente = id_cliente
        super().__init__(f"Cliente com ID {id_cliente} não encontrado.")