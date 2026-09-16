from datetime import datetime, timezone
from decimal import Decimal
from sqlalchemy import Numeric, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.core.database import Base


class LimiteContaModel(Base):
    __tablename__ = "limites_contas"

    id_limite: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True)
    id_conta: Mapped[int] = mapped_column(ForeignKey(
        "contas.id_conta", ondelete="CASCADE"), unique=True, nullable=False)
    limite_diario: Mapped[Decimal] = mapped_column(
        Numeric(15, 2), default=Decimal("5000.00"))
    limite_noturno: Mapped[Decimal] = mapped_column(
        Numeric(15, 2), default=Decimal("1000.00"))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    conta = relationship("ContaModel", back_populates="limites_contas")
