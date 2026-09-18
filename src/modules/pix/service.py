import uuid
from decimal import Decimal
from typing import Optional
from sqlalchemy.orm import IntegrityError

from src.modules.ledger.models import TipoTransacaoEnum
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

    def register_pix_key(self, id_conta: int, tipo_chave: str, valor_chave: Optional[str] = None) -> ChavePixModel:
        # 1. Cadastra a chave PIX para a conta especificada
        conta = self.conta_repo.search_account(id_conta)
        if not conta:
            raise ContaNaoEncontradaException(
                f"Conta com ID {id_conta} não encontrada.")

        # 2. Valida o tipo de chave
        valida_tipos = ["CPF", "EMAIL", "TELEFONE", "ALEATORIA"]
        tipo_upper = tipo_chave.upper()
        if tipo_upper not in valida_tipos:
            raise ValidaChavePixException(
                f"Tipo de chave '{tipo_chave}' inválido. Tipos aceitos: {valida_tipos}")

        # 3. Tratamento de valor para chave ALEATORIA (EVP) ou ausente
        if tipo_upper == "ALEATORIA" and not valor_chave:
            valor_chave = str(uuid.uuid4())
        elif not valor_chave:
            raise ValueError(
                "O valor da chave é obrigatório para este tipo de chave.")

        # 4. ersistência via Repository com captura de Violação de Unicidade
        try:
            nova_chave = self.pix_repo.create_pix_key( 
            id_conta=id_conta,
            tipo_chave=tipo_upper,
            valor_chave=valor_chave
        )
            self.db.commit()
            return nova_chave

        except IntegrityError:
            self.db.rollback()
            raise ChavePixDuplicadaException(
                f"Chave PIX '{valor_chave}' já está cadastrada.")
        except Exception:
            self.db.rollback()
            raise
        

    def make_pix_payment(
        self,
        id_conta_origem: int,
        id_conta_destino: Optional[int] = None,
        valor: Decimal = Decimal("0.00"),
        chave_destino: Optional[str] = None
    ):
        valor_decimal = Decimal(str(valor)) # Executa uma transferência PIX entre contas de forma atômica.
        if valor_decimal <= Decimal("0.00"):
            raise ValueError("O valor do PIX deve ser maior que zero.")

        # 1. Validação da conta de origem        
        conta_origem = self.conta_repo.search_account(id_conta_origem)
        if not conta_origem:
            raise ContaNaoEncontradaException(
                "Conta de origem não encontrada.")


        # 2. Resolve a conta de destino (prioriza chave se informada; caso contrário, usa o id)
        if chave_destino:
            chave_pix = self.pix_repo.search_account_by_key(chave_destino)
            if not chave_pix:
                raise ContaNaoEncontradaException(
                    "Chave PIX de destino não encontrada.")
            id_conta_destino = chave_pix.id_conta

        if not id_conta_destino:
            raise ContaNaoEncontradaException(
                "Conta de destino não informada.")

        conta_destino = self.conta_repo.search_account(id_conta_destino)
        if not conta_destino:
            raise ContaNaoEncontradaException(
                "Conta de destino não encontrada.")

        if id_conta_origem == id_conta_destino:
            raise ValueError(
                "Não é possível realizar transferência PIX para a mesma conta.")

        # 3. Execução da Transação Financeira Atômica (ACID)
        try:
            debito_sucesso = self.pix_repo.debit_with_lock(id_conta_origem, valor_decimal)
            if not debito_sucesso:
                raise SaldoInsuficienteException(
                    "Saldo insuficiente para realizar o PIX.")

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
