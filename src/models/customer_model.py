from sqlalchemy import Column, Integer, String, Date, CHAR
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
