from sqlalchemy import Column, Integer, String, ForeignKey
from src.core.database import Base


class TelefoneModel(Base):
    __tablename__ = "telefone"

    id_telefone = Column(Integer, primary_key=True)
    id_cliente = Column(Integer, ForeignKey(
        "cliente.id_cliente"), nullable=False)
    numero = Column(String(15), nullable=False)
    tipo = Column(String, nullable=False, default="CELULAR")
