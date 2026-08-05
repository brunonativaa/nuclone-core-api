from sqlalchemy import Column, Integer, Numeric, DateTime, ForeignKey
from src.core.database import Base


class SaldoContaModel(Base):
    __tablename__ = "saldo_conta"

    id_saldo_conta = Column(Integer, primary_key=True)
    id_conta = Column(Integer, ForeignKey("conta.id_conta"),
                      unique=True, nullable=False)
    saldo_disponivel = Column(Numeric(15, 2), nullable=False)
    saldo_bloqueado = Column(Numeric(15, 2), nullable=False, default=0.00)
    ultima_atualizacao = Column(DateTime)
