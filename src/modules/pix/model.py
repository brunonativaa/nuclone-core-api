import enum
from sqlalchemy import Column, Integer, String, Enum as SQLEnum, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from src.core.database import Base


class TypeChaveEnum(str, enum.Enum):
    CPF = "CPF"
    EMAIL = "EMAIL"
    TELEFONE = "TELEFONE"
    ALEATORIA = "ALEATORIA"


class KeyPixModel(Base):
    __tablename__ = "chaves_pix"

    id_chave = Column(Integer, primary_key=True, autoincrement=True)
    id_conta = Column(Integer, ForeignKey(
        "conta.id_conta", ondelete="CASCADE"), nullable=False)
    tipo_chave = Column(
        SQLEnum(TypeChaveEnum, name="typekeyenum"), nullable=False)
    valor_chave = Column(String(255), unique=True, nullable=False, index=True)
    criado_em = Column(DateTime(timezone=True),
                       server_default=func.now(), nullable=False)

    conta = relationship("ContaModel", back_populates="chaves_pix")
