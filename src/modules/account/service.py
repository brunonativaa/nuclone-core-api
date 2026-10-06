import random
from typing import Union
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.account.model import ContaModel, SaldoContaModel
from src.modules.account.repository import ContaRepository
from src.modules.account.schema import AccountCreateInput
from src.modules.customer.repository import ClienteRepository


class ContaNaoEncontradaException(Exception):
    pass


class ClienteNaoEncontradoException(Exception):
    pass


class ContaService:

    def __init__(self, db):
        self.db = db
        self.conta_repo = ContaRepository(db)
        self.cliente_repo = ClienteRepository(db)

    def _gerar_num_conta(self) -> str:
            return str(random.randint(100000, 999999))
    
    async def create_account(self, data_conta: Union[AccountCreateInput, dict]) -> ContaModel:
            # Conversão polimórfica: aceita Pydantic DTO ou dict
            payload = (
                data_conta.model_dump()
                if isinstance(data_conta, BaseModel)
                else data_conta.copy()
            )

            id_cliente = payload.get("id_cliente")

            # 1. Validação da Regra de Negócio
            cliente = await self.cliente_repo.get_by_id(id_cliente)
            if not cliente:
                raise ClienteNaoEncontradoException(f"Cliente {id_cliente} não encontrado.")

            # 2. Regras de preenchimento (Defensive Default Values)
            if not payload.get("num_conta"):
                payload["num_conta"] = self._gerar_num_conta()

            if not payload.get("agencia"):
                payload["agencia"] = "0001"

            try:
                # 3. Transação Atômica
                nova_conta =  await self.conta_repo.create_account(payload)
                await self.conta_repo.create_balance(nova_conta.id_conta)

                await self.db.commit()
                await self.db.refresh(nova_conta)

                # Retorna estritamente a entidade do ORM
                return nova_conta

            except Exception as e:
                
                await self.db.rollback()
                raise e

    async def get_by_id(self, id_conta: int) -> ContaModel:
        conta = await self.conta_repo.search_account(id_conta)
        if not conta:
            raise ContaNaoEncontradaException(
                f"Conta com ID {id_conta} não encontrada."
            )
        return conta

    async def get_balance(self, id_conta: int) -> SaldoContaModel:
        # 1. Verifica se a conta existe
        conta = await self.conta_repo.search_account(id_conta)
        if not conta:
            raise ContaNaoEncontradaException(f"A conta com ID {id_conta} não foi encontrada.")
        
        # 2. Busca o saldo associado no repositório
        saldo = await self.conta_repo.get_balance(id_conta)

        # 3. Regra de Negócio Fallback: Se o saldo não existir, inicializa e persiste
        if not saldo:
            saldo = await self.conta_repo.create_balance(id_conta)
            await self.db.commit()
            await self.db.refresh(saldo)

        return saldo