import enum
from datetime import datetime
from sqlalchemy import Column, Integer, Numeric, DateTime, String, ForeignKey, func, Enum
from src.core.database import Base


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
