from datetime import datetime
from sqlalchemy import Column, Integer, Numeric, DateTime, String, ForeignKey, func
from src.core.database import Base


class TransacaoModel(Base):
    __tablename__ = "transacao"

    id_transacao = Column(Integer, primary_key=True)
    id_conta_origem = Column(Integer, ForeignKey(
        "conta.id_conta"), nullable=False)
    id_conta_destino = Column(Integer, ForeignKey(
        "conta.id_conta"), nullable=False)
    tipo_transacao = Column(String, nullable=False, default="PIX")
    valor = Column(Numeric(15, 2), nullable=False)
    ultima_atualizacao = Column(DateTime, server_default=func.now())
