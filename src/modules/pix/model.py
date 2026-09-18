import enum
from datetime import datetime, timezone
from sqlalchemy import Integer, String, Enum as SQLEnum, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.core.database import Base


class TipoChavePixEnum(str, enum.Enum):
    CPF = "CPF"
    EMAIL = "EMAIL"
    TELEFONE = "TELEFONE"
    ALEATORIA = "ALEATORIA"


class ChavePixModel(Base):
    __tablename__ = "chaves_pix"

    id_chave: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    id_conta: Mapped[int] = mapped_column(Integer, ForeignKey(
        "contas.id_conta", ondelete="CASCADE"), nullable=False)
    tipo_chave: Mapped[TipoChavePixEnum] = mapped_column(
        SQLEnum(TipoChavePixEnum), nullable=False)
    valor_chave: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(
            DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    conta = relationship("ContaModel", back_populates="chaves_pix")
