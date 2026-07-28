from sqlalchemy import Column, Integer, String, ForeignKey
from src.core.database import Base


class ContaModel(Base):
    __tablename__ = "conta"

    id_conta = Column(Integer, primary_key=True)
    id_cliente = Column(Integer, ForeignKey(
        "cliente.id_cliente"), nullable=False)
    num_conta = Column(String(20), unique=True, nullable=False)
    tipo_conta = Column(String, nullable=False, default="PF")
    agencia = Column(String(10), nullable=False)
