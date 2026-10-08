from typing import Optional
from decimal import Decimal
import random
from typing import Union
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.account.model import ContaModel, SaldoContaModel
from src.modules.account.repository import ContaRepository
from src.modules.account.schema import AccountCreateInput
from src.modules.account.exceptions import ContaNaoEncontradaException, ClienteNaoEncontradoException
from src.modules.pix.exceptions import SaldoInsuficienteException
from src.modules.customer.repository import ClienteRepository



class ContaService:

    def __init__(self, db_session: AsyncSession, conta_repo: Optional[ContaRepository] = None, cliente_repo: Optional[ClienteRepository] = None):

        self.db = db_session 
        self.conta_repo = conta_repo or ContaRepository(db_session)
        self.cliente_repo = cliente_repo or ClienteRepository(db_session)

    async def create_account(self, id_cliente: int, agencia: str = "0001", tipo_conta: str = "PF") -> ContaModel:
        # Gera um número de conta único de 6 dígitos
            num_conta = str(random.randint(100000, 999999))

            conta = await self.conta_repo.create_account(
                id_cliente=id_cliente,
                agencia=agencia,
                num_conta=num_conta,
                tipo_conta=tipo_conta,
            )

            # Inicializa o registro de saldo na tabela correspondente
            await self.conta_repo.create_balance(id_conta=conta.id_conta)

            return conta

    async def get_by_id(self, id_conta: int) -> ContaModel:
        conta = await self.conta_repo.get_account_by_id(id_conta)
       
        if not conta:
            raise ContaNaoEncontradaException(f"Conta com ID {id_conta} não encontrada.")
        return conta

    async def get_balance(self, id_conta: int) -> SaldoContaModel:
        # 1. Garante que a conta existe
        await self.get_by_id(id_conta)

        # 2. Busca saldo
        saldo = await self.conta_repo.get_balance(id_conta)

        # 3. Fallback: cria saldo se não existir
        if not saldo:
            saldo = await self.conta_repo.create_balance(id_conta)
            await self.db.commit()
            await self.db.refresh(saldo)

        return saldo

    async def credit(self, id_conta: int, valor: Decimal) -> SaldoContaModel:
       
        if valor <= Decimal("0"):
            raise ValueError("O valor adicionado deve ser maior que zero.")

        saldo = await self.get_balance(id_conta)
        novo_saldo = saldo.saldo_disponivel + valor
        
        saldo_atualizado = await self.conta_repo.update_balance_value(saldo, novo_saldo)
        return saldo_atualizado

    async def debit_with_lock(self, id_conta: int, valor: Decimal) -> SaldoContaModel:
       
        if valor <= Decimal("0"):
            raise ValueError("O valor do débito deve ser maior que zero.")

        # Busca com bloqueio pessimista
        saldo = await self.conta_repo.get_balance_for_update(id_conta)
        if not saldo:
            raise ContaNaoEncontradaException(f"Conta com ID {id_conta} não encontrada.")

        # Validação da regra de negócio
        if saldo.saldo_disponivel < valor:
            raise SaldoInsuficienteException("Saldo insuficiente para realizar a transação.")

        novo_saldo = saldo.saldo_disponivel - valor
        return await self.conta_repo.update_balance_value(saldo, novo_saldo)