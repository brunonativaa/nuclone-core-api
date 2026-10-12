from typing import Sequence, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.customer.model import ClienteModel
from src.modules.customer.exceptions import ClienteNaoEncontradoException


class ClienteRepository:

    def __init__(self, db_session: AsyncSession):
        self.db = db_session

    async def create(self, data: dict) -> ClienteModel:
        cliente = ClienteModel(**data)
        self.db.add(cliente)
        await self.db.flush()  # Envia os comandos SQL para a transação atual para gerar o ID
        await self.db.refresh(cliente)
        return cliente

    async def get_all(self) -> Sequence[ClienteModel]:
        stmt = select(ClienteModel)
        return (await self.db.scalars(stmt)).all()  # db.scalars() desempacota as linhas retornadas, entregando a lista de objetos ClienteModel

    async def get_by_cpf(self, cpf: str) -> ClienteModel | None:
       stmt = select(ClienteModel).where(ClienteModel.cpf == cpf) # db.scalar() executa a query e retorna o primeiro objeto encontrado ou None
       return (await self.db.scalar(stmt))
    
    async def get_by_id(self, id_cliente: int) -> Optional[ClienteModel]:
        
        return await self.db.get(ClienteModel, id_cliente)