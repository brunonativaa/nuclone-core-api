from typing import Optional
from sqlalchemy.orm import Session
from src.modules.customer.model import ClienteModel
from src.modules.account.model import ContaModel

class AuthRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_cliente_by_email(self, email: str) -> Optional[ClienteModel]:
        return self.db.query(ClienteModel).filter(ClienteModel.email == email).first()  

    def get_account_by_cliente_id(self, id_cliente: int) -> Optional[ContaModel]:
        return self.db.query(ContaModel).filter(ContaModel.id_cliente == id_cliente).first()
    