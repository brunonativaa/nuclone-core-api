from datetime import datetime, timezone
from decimal import Decimal
import enum
from sqlalchemy import Integer, Numeric, DateTime, TIMESTAMP, Boolean, ForeignKey, Enum as SQLEnum
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
        SQLEnum(TipoTransacaoEnum,name="tipo_de_transacao"), default=TipoTransacaoEnum.PIX, server_default=TipoTransacaoEnum.PIX, nullable=False)
    valor: Mapped[Decimal] = mapped_column(
        Numeric(15, 2), default=Decimal('0.00'), nullable=False)
    status: Mapped[StatusTransacaoEnum] = mapped_column(
        SQLEnum(StatusTransacaoEnum,name="tipo_de_status"), default=StatusTransacaoEnum.CONCLUIDO, server_default=StatusTransacaoEnum.CONCLUIDO.value, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    is_noturno: Mapped[bool] = mapped_column(
        Boolean, 
        default=False, 
        nullable=False, 
        server_default="false", 
        comment="Flag que indica se a transação ocorreu no período noturno (20h às 06h)"
    )
