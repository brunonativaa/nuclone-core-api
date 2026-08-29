from sqlalchemy import Column, Integer, String, Date, CHAR, ForeignKey
from sqlalchemy.orm import relationship
from src.core.database import Base


class ClienteModel(Base):
    __tablename__ = 'cliente'

    id_cliente = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    cpf = Column(String(11), unique=True, nullable=False)
    sexo = Column(CHAR(1))
    email = Column(String(100), unique=True, nullable=False)
    senha = Column(String(60), nullable=False)
    data_nascimento = Column(Date, nullable=False)

    endereco = relationship("EnderecoModel", back_populates="cliente")
    telefone = relationship("TelefoneModel", back_populates="cliente")


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

    cliente = relationship("ClienteModel", back_populates="endereco")


class TelefoneModel(Base):
    __tablename__ = "telefone"

    id_telefone = Column(Integer, primary_key=True)
    id_cliente = Column(Integer, ForeignKey(
        "cliente.id_cliente"), nullable=False)
    numero = Column(String(15), nullable=False)
    tipo = Column(String, nullable=False, default="CELULAR")

    cliente = relationship("ClienteModel", back_populates="telefone")
