# fmt: off
# noqa: E402

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=True, future=True)

Base = declarative_base()

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    future=True
)

from src.models.customer_model import ClienteModel
from src.models.account_model import ContaModel
from src.models.balance_account_model import SaldoContaModel
from src.models.transaction_model import TransacaoModel
from src.models.address_model import EnderecoModel
from src.models.telephone_model import TelefoneModel

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
