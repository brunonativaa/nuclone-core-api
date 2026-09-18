from datetime import datetime, timezone
from decimal import Decimal
import enum
from sqlalchemy import Integer, Numeric, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column
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
        Integer, primary_key=True, autoincrement=True)
    id_conta_origem: Mapped[int] = mapped_column(
        ForeignKey("contas.id_conta"), nullable=False, index=True)
    id_conta_destino: Mapped[int] = mapped_column(
        ForeignKey("contas.id_conta"), nullable=False, index=True)
    tipo_transacao: Mapped[TipoTransacaoEnum] = mapped_column(
        SQLEnum(TipoTransacaoEnum, default=TipoTransacaoEnum.PIX))
    valor: Mapped[Decimal] = mapped_column(
        Numeric(15, 2), default=Decimal('0.00'), nullable=False)
    status: Mapped[StatusTransacaoEnum] = mapped_column(
        SQLEnum(StatusTransacaoEnum,name="status_transacao"), default=StatusTransacaoEnum.CONCLUIDO, server_default=StatusTransacaoEnum.CONCLUIDO.value, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
