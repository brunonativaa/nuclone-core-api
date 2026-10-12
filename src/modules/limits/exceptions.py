from decimal import Decimal

class LimitException(Exception):
    """Exceção base para erros relacionados a limites."""
    pass

class LimitNotFoundException(LimitException):
    def __init__(self, message: str = "Configuração de limites não encontrada."):
        self.message = message
        super().__init__(self.message)

class ExceededLimitException(LimitException):
    def __init__(self, message: str = "Transação excede o limite disponível.", disponivel: Decimal):
        self.message = message
        self.disponivel = disponivel
        super().__init__(self.message)    
