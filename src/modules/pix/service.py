import uuid

from decimal import Decimal
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from src.modules.limits.service import LimitesService
from src.modules.limits.repository import LimitesRepository
from src.modules.ledger.repository import LedgerRepository 
from src.modules.ledger.model import TransacaoModel, TipoTransacaoEnum
from src.modules.account.repository import ContaRepository
from src.modules.account.service import ContaService
from src.modules.pix.repository import PixRepository
from src.modules.pix.model import ChavePixModel
from src.modules.pix.exceptions import (
    SaldoInsuficienteException,
    ContaNaoEncontradaException,
    ChavePixDuplicadaException,
    ValidaChavePixException
)


class PixService:

    def __init__(self, db: AsyncSession):
        self.db = db
        self.conta_service = ContaService(db)
        self.conta_repo = ContaRepository(db)
        self.pix_repo = PixRepository(db)
        self.limits_repo = LimitesRepository(db)
        self.ledger_repo = LedgerRepository(db)


    async def register_pix_key(self, id_conta: int, key_type: str, valor_chave: Optional[str] = None) -> ChavePixModel:
        # 1. Cadastra a chave PIX para a conta especificada
        conta = await self.conta_repo.get_account_by_id(id_conta)
        if not conta:
            raise ContaNaoEncontradaException(
                f"Conta com ID {id_conta} não encontrada.")

        # 2. Valida o tipo de chave
        valida_tipos = ["CPF", "EMAIL", "TELEFONE", "ALEATORIA"]
        tipo_upper = key_type.upper()
        if tipo_upper not in valida_tipos:
            raise ValidaChavePixException(
                f"Tipo de chave '{key_type}' inválido. Tipos aceitos: {valida_tipos}")

        # 3. Tratamento de valor para chave ALEATORIA (EVP) ou ausente
        if tipo_upper == "ALEATORIA" and not valor_chave:
            valor_chave = str(uuid.uuid4())
        elif not valor_chave:
            raise ValueError(
                "O valor da chave é obrigatório para este tipo de chave.")

        # 4. Verificação prévia de existência da chave
        chave_existente = await self.pix_repo.get_key_by_value(valor_chave)
        if chave_existente:
            raise ChavePixDuplicadaException(
                f"Chave PIX '{valor_chave}' já está cadastrada.")
        
        # 5. Persistência
        try:
            nova_chave = await self.pix_repo.create_pix_key( 
            id_conta=id_conta,
            tipo_chave=tipo_upper,
            valor_chave=valor_chave
        )
            await self.db.commit()
            return nova_chave

        except IntegrityError as err:
            await self.db.rollback()
            # Inspeciona a causa real do IntegrityError
            err_msg = str(err.orig).lower() if hasattr(err, 'orig') else str(err).lower()
            if "unique" in err_msg or "duplicate" in err_msg:
                raise ChavePixDuplicadaException(f"Chave PIX '{valor_chave}' já está cadastrada.")
            if "foreign key" in err_msg or "fk" in err_msg:
                raise ContaNaoEncontradaException(f"Conta com ID {id_conta} não encontrada no banco de dados.")
            raise err
        except Exception:
            await self.db.rollback()
            raise
        

    async def make_pix_payment(self, id_conta_origem: int,id_conta_destino: Optional[int] = None, valor: Decimal = Decimal("0.00"),chave_destino: Optional[str] = None) -> TransacaoModel:
        
        valor_decimal = Decimal(str(valor)) # Executa uma transferência PIX entre contas de forma atômica.
        if valor_decimal <= Decimal("0.00"):
            raise ValueError("O valor do Pix deve ser maior que zero.")

        # 1. Validação da conta de origem        
        conta_origem = await self.conta_service.get_by_id(id_conta_origem)
        if not conta_origem:
            raise ContaNaoEncontradaException(id_conta_origem)

        limites_service = LimitesService(self.limits_repo, self.ledger_repo)
        await limites_service.validar_e_consumir_limite(
            id_conta=id_conta_origem,
            valor=valor_decimal
        )

        # 2. Resolução da conta de destino
        if chave_destino:
            conta_destino_obj = await self.pix_repo.search_account_by_key(chave_destino)
            if not conta_destino_obj:
                raise ContaNaoEncontradaException(id_conta_origem)
            id_conta_destino = conta_destino_obj.id_conta


        if not id_conta_destino:
            raise ValueError("Conta de destino não informada.")

        if id_conta_origem == id_conta_destino:
            raise ValueError("Não é possível realizar transferência PIX para a mesma conta.")

        # 3. Transação Atômica com Concorrência Tratada
        debito_sucesso = await self.conta_service.debit_with_lock(id_conta_origem, valor_decimal)
        if not debito_sucesso:
            raise SaldoInsuficienteException("Saldo insuficiente para realizar o PIX.")
        
        try:
            await self.conta_service.credit(id_conta_destino, valor_decimal)

            dados_transacao = await self.pix_repo.record_transaction({
                "id_conta_origem": id_conta_origem,
                "id_conta_destino": id_conta_destino,
                "tipo_transacao": TipoTransacaoEnum.PIX,
                "valor": valor_decimal
            })

            await self.db.commit()
            return dados_transacao

        except Exception as e:
            await self.db.rollback()
            raise e
