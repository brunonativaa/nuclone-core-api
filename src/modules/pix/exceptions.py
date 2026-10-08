class PixException(Exception):
    pass

class SaldoInsuficienteException(PixException):
    pass

class ContaNaoEncontradaException(PixException):
    pass


class ChavePixDuplicadaException(PixException):
    pass

class ValidaChavePixException(PixException):
    pass        
