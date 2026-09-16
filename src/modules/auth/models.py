from datetime import datetime
from tping import Optional
from sqlalchemy import String, DateTime, ForeignKey, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.core.database import Base


class AuthModel(Base):
    __tablename__ = "auth_credencials"

    id_auth: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    id_cliente: Mapped[int] = mapped_column(ForeignKey(
        "cliente.id_cliente"), ondelete="CASCADE", unique=True, nullable=False)
    senha_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    pin_transacao_hash: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=False)
    tentativas_falhas_login: Mapped[int] = mapped_column(
        Integer, default=0, nullable=False)
    tentativas_falhas_pin: Mapped[int] = mapped_column(
        Integer, default=0, nullable=False)
    conta_bloqueada: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False)

    ultimo_login: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    cliente = relationship("ClienteModel", back_populates="auth_credencials")
