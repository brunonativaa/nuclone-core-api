from src.core.exceptions import DomainException


class PixException(DomainException):
    """Exceção base para erros no módulo de PIX."""
    pass


class SaldoInsuficienteException(PixException):
    """Lançada quando a conta de origem não possui saldo suficiente."""
    def __init__(self, saldo_atual: str = None):
        msg = "Saldo insuficiente para realizar a transferência PIX."
        if saldo_atual is not None:
            msg += f" Saldo disponível: R$ {saldo_atual}."
        super().__init__(msg)


class ContaNaoEncontradaException(PixException):
    """Lançada quando a conta informada na transação PIX não é localizada."""
    def __init__(self, id_conta: int):
        self.id_conta = id_conta
        super().__init__(f"Conta com ID {id_conta} não encontrada para a transação PIX.")


class ChavePixDuplicadaException(PixException):
    """Lançada ao tentar cadastrar uma chave PIX já existente."""
    def __init__(self, chave: str):
        self.chave = chave
        super().__init__(f"A chave PIX '{chave}' já está cadastrada no sistema.")


class ValidaChavePixException(PixException):
    """Lançada quando o formato da chave PIX é inválido."""
    def __init__(self, chave: str, motivo: str):
        self.chave = chave
        super().__init__(f"Chave PIX '{chave}' inválida: {motivo}")