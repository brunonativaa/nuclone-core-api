class LedgerException(Exception):
    pass

class TransacaoNaoEncontradaException(LedgerException):
    def __init__(self, id_transacao: int):
        super().__init__(f"A transação com ID {id_transacao} não foi encontrada.")
        self.id_transacao = id_transacao

class LedgerInconsistenteException(LedgerException):
    def __init__(self, message: str = "Inconsistência detectada no ledger da conta."):
        super().__init__(message)


