from sqlalchemy.orm import Session
from src.models.cliente_model import ClienteModel


class ClienteRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, data):
        cliente = ClienteModel(**data)
        self.db.add(cliente)
        self.db.commit()
        self.db.refresh(cliente)
        return cliente

    def get_all(self):
        return self.db.query(ClienteModel).all()

    def get_by_id(self, id_cliente):
        return self.db.query(ClienteModel).filter_by(id_cliente=id_cliente).first()
