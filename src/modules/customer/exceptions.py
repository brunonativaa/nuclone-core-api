

class ClienteException(Exception):
    """Exceção base para erros relacionados a clientes."""
    pass

class ClienteJaExisteException(ClienteException):
    def __init__(self, message: str = "Já existe um cliente cadastrado."):
        self.message = message
        super().__init__(self.message)

class ClienteNaoEncontradoException(ClienteException):
    def __init__(self, message: str = "Cliente não encontrado."):
        self.message = message
        super().__init__(self.message)