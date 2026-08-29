import enum
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, DateTime, func, Enum
from sqlalchemy.orm import relationship
from src.core.database import Base


class ContaModel(Base):
    __tablename__ = "conta"

    id_conta = Column(Integer, primary_key=True)
    id_cliente = Column(Integer, ForeignKey(
        "cliente.id_cliente"), nullable=False)
    num_conta = Column(String(20), unique=True, nullable=False)
    tipo_conta = Column(String, nullable=False, default="PF")
    agencia = Column(String(10), nullable=False)

    transacoes_enviadas = relationship(
        "TransacaoModel",
        foreign_keys="[TransacaoModel.id_conta_origem]",
        back_populates="conta_origem"
    )

    transacoes_recebidas = relationship(
        "TransacaoModel",
        foreign_keys="[TransacaoModel.id_conta_destino]",
        back_populates="conta_destino"
    )

    saldo_conta = relationship("SaldoContaModel", back_populates="conta")


class TipoTransacaoEnum (str, enum.Enum):
    PIX = "PIX"
    TED = "TED"


class TransacaoModel(Base):
    __tablename__ = "transacao"

    id_transacao = Column(Integer, primary_key=True)
    id_conta_origem = Column(Integer, ForeignKey(
        "conta.id_conta"), nullable=False)
    id_conta_destino = Column(Integer, ForeignKey(
        "conta.id_conta"), nullable=False)
    tipo_transacao = Column(Enum(TipoTransacaoEnum, name="tipo_transacao",
                                 create_type=False), nullable=False, default=TipoTransacaoEnum.PIX)
    valor = Column(Numeric(15, 2), nullable=False)
    data_hora = Column(DateTime, server_default=func.now())

    conta_origem = relationship(
        "ContaModel",
        foreign_keys=[id_conta_origem],
        back_populates="transacoes_enviadas"
    )

    conta_destino = relationship(
        "ContaModel",
        foreign_keys=[id_conta_destino],
        back_populates="transacoes_recebidas"
    )


class SaldoContaModel(Base):
    __tablename__ = "saldo_conta"

    id_saldo_conta = Column(Integer, primary_key=True)
    id_conta = Column(Integer, ForeignKey("conta.id_conta"),
                      unique=True, nullable=False)
    saldo_disponivel = Column(Numeric(15, 2), nullable=False)
    saldo_bloqueado = Column(Numeric(15, 2), nullable=False, default=0.00)
    ultima_atualizacao = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    conta = relationship("ContaModel", back_populates="saldo_conta")
