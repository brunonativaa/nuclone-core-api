import enum
from datetime import datetime, timezone
from decimal import Decimal
from typing import TYPE_CHECKING, Optional, List
from sqlalchemy import String, ForeignKey, Numeric, DateTime, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.core.database import Base
from src.modules.limits.models import LimiteContaModel
from src.modules.pix.model import ChavePixModel


if TYPE_CHECKING:
    from src.modules.limits.models import LimiteContaModel
    from src.modules.customer.model import ClienteModel


class TipoContaEnum(str, enum.Enum):
    PF = "PF"
    PJ = "PJ"


class ContaModel(Base):

    __tablename__ = "contas"

    id_conta: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_cliente: Mapped[int] = mapped_column(ForeignKey(
        "clientes.id_cliente"), nullable=False)
    num_conta: Mapped[str] = mapped_column(
        String(20), nullable=False, unique=True)
    tipo_conta: Mapped[TipoContaEnum] = mapped_column(
        SQLEnum(TipoContaEnum), nullable=False, default=TipoContaEnum.PF)
    agencia: Mapped[str] = mapped_column(
        String(10), default="0001", nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    cliente: Mapped["ClienteModel"] = relationship(
        "ClienteModel", back_populates="contas")
    saldo: Mapped["SaldoContaModel"] = relationship("SaldoContaModel", back_populates="conta",
                                                    uselist=False, cascade="all, delete-orphan")
    limites: Mapped[Optional[LimiteContaModel]] = relationship(
        "LimiteContaModel", back_populates="conta", uselist=False, cascade="all, delete-orphan")
    chaves_pix: Mapped[List["ChavePixModel"]] = relationship(
        "ChavePixModel", back_populates="conta", cascade="all, delete-orphan")


class SaldoContaModel(Base):
    __tablename__ = "saldo_contas"

    id_saldo_conta: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True)
    id_conta: Mapped[int] = mapped_column(ForeignKey("contas.id_conta"),
                                          unique=True, nullable=False)
    saldo_disponivel: Mapped[Decimal] = mapped_column(
        Numeric(15, 2), nullable=False, default=Decimal('0.00'))
    saldo_bloqueado: Mapped[Decimal] = mapped_column(
        Numeric(15, 2), nullable=False, default=Decimal('0.00'))
    ultima_atualizacao: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    conta: Mapped["ContaModel"] = relationship(
        "ContaModel", back_populates="saldo")
