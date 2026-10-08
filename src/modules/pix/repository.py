from decimal import Decimal
from typing import Optional
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.account.model import ContaModel,  SaldoContaModel
from src.modules.customer.model import ClienteModel, TelefoneModel
from src.modules.ledger.model import TransacaoModel, TipoTransacaoEnum
from src.modules.pix.model import ChavePixModel


class PixRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_key_by_value(self, valor_chave: str) -> Optional[ChavePixModel]:
        """Busca uma chave PIX específica pelo seu valor."""
     
        stmt = select(ChavePixModel).where(ChavePixModel.valor_chave == valor_chave)
        return await self.db.scalar(stmt)

    async def create_pix_key(self, id_conta: int, tipo_chave: str, valor_chave: str) -> ChavePixModel:
        """
        Instancia e adiciona a nova Chave PIX na sessão da ORM.
        Nota: Não executa commit() aqui para permitir controle transacional (Unit of Work) na camada de Service.
        """
       
        nova_chave = ChavePixModel(
            id_conta=id_conta,
            tipo_chave=tipo_chave,
            valor_chave=valor_chave
        )
        self.db.add(nova_chave)
        await self.db.flush() # Flush para obter o ID da chave PIX gerada na transação ativa
        return nova_chave

    async def search_account_by_key(self, chave_pix: str) -> Optional[ContaModel]:
        """Busca a conta associada a uma chave PIX, CPF, e-mail ou telefone."""
        stmt = (
            select(ContaModel)
            .join(ChavePixModel, ContaModel.id_conta == ChavePixModel.id_conta)
            .join(ClienteModel, ContaModel.id_cliente == ClienteModel.id_cliente)
            .outerjoin(TelefoneModel, ClienteModel.id_cliente == TelefoneModel.id_cliente)
            .where(
                or_(
                    ChavePixModel.valor_chave == chave_pix,
                    ClienteModel.cpf == chave_pix,
                    ClienteModel.email == chave_pix,
                    TelefoneModel.numero == chave_pix
                )
            )
        )
        return await self.db.scalar(stmt)
        # Passa o valor positivo para somar
        return await self.update_saldo(id_conta, Decimal(str(valor)))

    async def record_transaction(self, data: dict) -> TransacaoModel:
        transacao = TransacaoModel(
            id_conta_origem=data["id_conta_origem"],
            id_conta_destino=data["id_conta_destino"],
            tipo_transacao=data["tipo_transacao"],
            valor=data["valor"]
        )
        self.db.add(transacao)
        await self.db.flush()
        return transacao
