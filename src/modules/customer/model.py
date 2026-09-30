import enum
from sqlalchemy import Integer, String, Date, CHAR, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.core.database import Base
from src.modules.account.model import ContaModel


class ClienteModel(Base):
    __tablename__ = 'clientes'

    id_cliente: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    cpf: Mapped[str] = mapped_column(String(11), unique=True, nullable=False)
    sexo: Mapped[str] = mapped_column(CHAR(1))
    email: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False)
    senha_hash: Mapped[str] = mapped_column(String(60), nullable=False)
    pin_transacao_hash: Mapped[str] = mapped_column(
        String(60), nullable=False)
    data_nascimento: Mapped[Date] = mapped_column(Date, nullable=False)

    contas: Mapped[list["ContaModel"]] = relationship(
        "ContaModel", back_populates="cliente", cascade="all, delete-orphan")
    endereco: Mapped["EnderecoModel"] = relationship(
        "EnderecoModel", back_populates="cliente")
    telefone: Mapped[list["TelefoneModel"]] = relationship(
        "TelefoneModel", back_populates="cliente", cascade="all, delete-orphan")


class TipoNumeroEnum(str, enum.Enum):
    CELULAR = "CELULAR"
    FIXO = "RESIDENCIAL"
    COMERCIAL = "COMERCIAL"


class EnderecoModel(Base):
    __tablename__ = 'enderecos'

    id_endereco: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True)
    id_cliente: Mapped[int] = mapped_column(Integer, ForeignKey(
        "clientes.id_cliente"), nullable=False)
    estado: Mapped[str] = mapped_column(String(2), nullable=False)
    cidade: Mapped[str] = mapped_column(String(100), nullable=False)
    bairro: Mapped[str] = mapped_column(String(100), nullable=False)
    rua: Mapped[str] = mapped_column(String(150), nullable=False)
    cep: Mapped[str] = mapped_column(String(8), nullable=False)
    num: Mapped[str] = mapped_column(String(10), nullable=False)

    cliente = relationship("ClienteModel", back_populates="endereco")


class TelefoneModel(Base):
    __tablename__ = "telefones"

    id_telefone: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_cliente: Mapped[int] = mapped_column(Integer, ForeignKey(
        "clientes.id_cliente"), nullable=False)
    numero: Mapped[str] = mapped_column(String(15), nullable=False)
    tipo: Mapped[TipoNumeroEnum] = mapped_column(
        SQLEnum(TipoNumeroEnum), nullable=False, default=TipoNumeroEnum.CELULAR)

    cliente = relationship("ClienteModel", back_populates="telefone")
