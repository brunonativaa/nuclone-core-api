from datetime import datetime, timezone
from decimal import Decimal
import enum
from sqlalchemy import String, Numeric, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.core.database import Base


class TipoTransacaoEnum(str, enum.Enum):
    PIX = "PIX"
    TED = "TED"
    DOC = "DOC"
    ESTORNADO = "ESTORNO"


class StatusTransacaoEnum(str, enum.Enum):
    CONCLUIDO = "CONCLUIDO"
    PENDENTE = "PENDENTE"
    CANCELADO = "CANCELADO"
    ESTORNADO = "ESTORNADO"
    FALHOU = "FALHOU"


class TransacaoModel(Base):
    __tablename__ = "transacao"

    id_transacao: Mapped[int] = mapped_column(
        String(36), primary_key=True, autoincrement=True)
    id_conta_origem: Mapped[int] = mapped_column(
        ForeignKey("contas.id_conta"), nullable=False)
    id_conta_destino: Mapped[int] = mapped_column(
        ForeignKey("contas.id_conta"), nullable=False)
    tipo_transacao: Mapped[TipoTransacaoEnum] = mapped_column(
        SQLEnum(TipoTransacaoEnum, default=TipoTransacaoEnum.PIX))
    valor: Mapped[Decimal] = mapped_column(
        Numeric(15, 2), default=Decimal('0.00'), nullable=False)
    status: Mapped[StatusTransacaoEnum] = mapped_column(
        SQLEnum(StatusTransacaoEnum, default=StatusTransacaoEnum.CONCLUIDO))
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
