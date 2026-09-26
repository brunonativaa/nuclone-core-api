import uuid
from decimal import Decimal
from typing import Optional
from sqlalchemy.exc import IntegrityError

from src.modules.ledger.model import TransacaoModel, TipoTransacaoEnum
from src.modules.account.repository import ContaRepository
from src.modules.pix.repository import PixRepository
from src.modules.pix.model import ChavePixModel


class PixException(Exception):
    pass

class SaldoInsuficienteException(PixException):
    pass


class ContaNaoEncontradaException(PixException):
    pass


class ChavePixDuplicadaException(PixException):
    pass

class ValidaChavePixException(PixException):
    pass


class PixService:

    def __init__(self, db):
        self.db = db
        self.conta_repo = ContaRepository(db)
        self.pix_repo = PixRepository(db)

    def register_pix_key(self, id_conta: int, key_type: str, valor_chave: Optional[str] = None) -> ChavePixModel:
        # 1. Cadastra a chave PIX para a conta especificada
        conta = self.conta_repo.search_account(id_conta)
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
        chave_existente = self.pix_repo.get_key_by_value(valor_chave)
        if chave_existente:
            raise ChavePixDuplicadaException(
                f"Chave PIX '{valor_chave}' já está cadastrada.")
        
        # 5. Persistência
        try:
            nova_chave = self.pix_repo.create_pix_key( 
            id_conta=id_conta,
            tipo_chave=tipo_upper,
            valor_chave=valor_chave
        )
            self.db.commit()
            return nova_chave

        except IntegrityError as err:
            self.db.rollback()
            # Inspeciona a causa real do IntegrityError
            err_msg = str(err.orig).lower() if hasattr(err, 'orig') else str(err).lower()
            if "unique" in err_msg or "duplicate" in err_msg:
                raise ChavePixDuplicadaException(f"Chave PIX '{valor_chave}' já está cadastrada.")
            if "foreign key" in err_msg or "fk" in err_msg:
                raise ContaNaoEncontradaException(f"Conta com ID {id_conta} não encontrada no banco de dados.")
            raise err
        except Exception:
            self.db.rollback()
            raise
        

    def make_pix_payment(
        self,
        id_conta_origem: int,
        id_conta_destino: Optional[int] = None,
        valor: Decimal = Decimal("0.00"),
        chave_destino: Optional[str] = None
    ) -> TransacaoModel:
        
        valor_decimal = Decimal(str(valor)) # Executa uma transferência PIX entre contas de forma atômica.
        if valor_decimal <= Decimal("0.00"):
            raise ValueError("O valor do PIX deve ser maior que zero.")

        # 1. Validação da conta de origem        
        conta_origem = self.conta_repo.search_account(id_conta_origem)
        if not conta_origem:
            raise ContaNaoEncontradaException(
                "Conta de origem não encontrada.")


        # 2. Resolução da conta de destino
        if chave_destino:
            conta_destino_obj = self.pix_repo.search_account_by_key(chave_destino)
            if not conta_destino_obj:
                raise ContaNaoEncontradaException("Chave PIX de destino não encontrada.")
            id_conta_destino = conta_destino_obj.id_conta

        if not id_conta_destino:
            raise ContaNaoEncontradaException("Conta de destino não informada.")

        conta_destino = self.conta_repo.search_account(id_conta_destino)
        if not conta_destino:
            raise ContaNaoEncontradaException("Conta de destino não encontrada.")

        if id_conta_origem == id_conta_destino:
            raise ValueError("Não é possível realizar transferência PIX para a mesma conta.")

        # 3. Transação Atômica com Concorrência Tratada
        debito_sucesso = self.pix_repo.debit_with_lock(id_conta_origem, valor_decimal)
        if not debito_sucesso:
            raise SaldoInsuficienteException("Saldo insuficiente para realizar o PIX.")
        
        try:
            self.pix_repo.credit(id_conta_destino, valor_decimal)

            dados_transacao = self.pix_repo.record_transaction({
                "id_conta_origem": id_conta_origem,
                "id_conta_destino": id_conta_destino,
                "tipo_transacao": TipoTransacaoEnum.PIX,
                "valor": valor_decimal
            })

            self.db.commit()
            return dados_transacao

        except Exception as e:
            self.db.rollback()
            raise e

    def adding_balance(self, id_conta: int, valor: Decimal):
        valor_decimal = Decimal(str(valor))

        if valor_decimal <= 0:
            raise ValueError("O valor adicionado deve ser maior que zero.")

        conta = self.conta_repo.search_account(id_conta)
        if not conta:
            raise ContaNaoEncontradaException("Conta não encontrada.")

        try:
            saldo_atualizado = self.pix_repo.credit(id_conta, valor_decimal)
            self.db.commit()
            return saldo_atualizado

        except Exception as e:
            self.db.rollback()
            raise e
