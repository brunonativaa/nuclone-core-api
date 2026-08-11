from sqlalchemy.orm import Session
from src.models.customer_model import ClienteModel


class ClienteRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, data: dict) -> ClienteModel:
        cliente = ClienteModel(**data)
        self.db.add(cliente)
        self.db.flush()  # Gera o ID e envia pro banco sem efetivar o commit ainda
        self.db.refresh(cliente)
        return cliente

    def get_all(self):
        return self.db.query(ClienteModel).all()

    def get_by_cpf(self, cpf: str) -> ClienteModel | None:
        return self.db.query(ClienteModel).filter(ClienteModel.cpf == cpf).first()

    def get_by_id(self, id_cliente: int) -> ClienteModel | None:
        return self.db.query(ClienteModel).filter_by(id_cliente=id_cliente).first()
