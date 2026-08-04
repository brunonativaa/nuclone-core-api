from sqlalchemy import Column, Integer, String, ForeignKey
from src.core.database import Base


class EnderecoModel(Base):
    __tablename__ = 'endereco'

    id_endereco = Column(Integer, primary_key=True, index=True)
    id_cliente = Column(Integer, ForeignKey(
        "cliente.id_cliente"), nullable=False)
    estado = Column(String(2), nullable=False)
    cidade = Column(String(100), nullable=False)
    bairro = Column(String(100), nullable=False)
    rua = Column(String(150), nullable=False)
    cep = Column(String(8), nullable=False)
    num = Column(String(10), nullable=False)
