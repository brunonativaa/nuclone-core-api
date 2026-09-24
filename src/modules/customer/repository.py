from typing import Sequence
from sqlalchemy import select
from sqlalchemy.orm import Session
from src.modules.customer.model import ClienteModel


class ClienteRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, data: dict) -> ClienteModel:
        cliente = ClienteModel(**data)
        self.db.add(cliente)
        self.db.flush()  # Envia os comandos SQL para a transação atual para gerar o ID
        self.db.refresh(cliente)
        return cliente

    def get_all(self) -> Sequence[ClienteModel]:
        stmt = select(ClienteModel)
        return self.db.scalars(stmt).all()  # db.scalars() desempacota as linhas retornadas, entregando a lista de objetos ClienteModel

    def get_by_cpf(self, cpf: str) -> ClienteModel | None:
       stmt = select(ClienteModel).where(ClienteModel.cpf == cpf) # db.scalar() executa a query e retorna o primeiro objeto encontrado ou None
       return self.db.scalar(stmt)

    def get_by_id(self, id_cliente: int) -> ClienteModel | None:
        return self.db.get(ClienteModel, id_cliente) # Para busca por Chave Primária, o db.get() é a forma nativa mais eficiente do ORM 2.0
