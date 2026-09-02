from decimal import Decimal
from typing import Optional
import uuid
from src.modules.account.model import TipoTransacaoEnum
from src.modules.account.repository import ContaRepository
from src.modules.pix.repository import PixRepository, KeyPixModel


class SaldoInsuficienteException(Exception):
    pass


class ContaNaoEncontradaException(Exception):
    pass


class PixService:

    def __init__(self, db):
        self.db = db
        self.conta_repo = ContaRepository(db)
        self.pix_repo = PixRepository(db)

    def register_pix_key(self, id_conta: int, key_type: str, valor_chave: str = None) -> KeyPixModel:
        # 1. Valida se a conta existe via Repository
        conta = self.conta_repo.search_account(id_conta)
        if not conta:
            raise ContaNaoEncontradaException(
                f"Conta com ID {id_conta} não encontrada.")

        # 2. Valida o tipo de chave
        valid_types = ["CPF", "EMAIL", "TELEFONE", "ALEATORIA"]
        tipo_upper = key_type.upper()
        if tipo_upper not in valid_types:
            raise ValueError(
                f"Tipo de chave '{key_type}' inválido. Tipos aceitos: {valid_types}")

        # 3. Tratamento de valor para chave ALEATORIA (EVP) ou ausente
        if tipo_upper == "ALEATORIA" and not valor_chave:
            valor_chave = str(uuid.uuid4())
        elif not valor_chave:
            raise ValueError(
                "O valor da chave é obrigatório para este tipo de chave.")

        # 4. Instancia a Model da chave Pix
        new_key = KeyPixModel(
            id_conta=id_conta,
            tipo_chave=tipo_upper,
            valor_chave=valor_chave
        )

        # 5. Persiste no banco de dados com commit/rollback
        try:
            self.db.add(new_key)
            self.db.commit()
            self.db.refresh(new_key)
            return new_key
        except Exception as e:
            self.db.rollback()
            raise e

    def make_pix_payment(
        self,
        id_conta_origem: int,
        id_conta_destino: Optional[int] = None,
        valor: Decimal = Decimal("0.00"),
        chave_destino: Optional[str] = None
    ):
        valor_decimal = Decimal(str(valor))

        # 1. Valida conta de origem
        conta_origem = self.conta_repo.search_account(id_conta_origem)
        if not conta_origem:
            raise ContaNaoEncontradaException(
                "Conta de origem não encontrada.")

        # --- Validação de Saldo ----
        # Busca o saldo atual no serviço/repositório de contas
        saldo_origem = self.conta_repo.get_saldo(id_conta_origem)
        if not saldo_origem or saldo_origem.saldo_disponivel < valor_decimal:
            raise SaldoInsuficienteException(
                "Saldo insuficiente para realizar o PIX.")

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

        # 3. Impede auto-transferência
        if id_conta_origem == id_conta_destino:
            raise ValueError(
                "Não é possível realizar transferência PIX para a mesma conta.")

        # 4. Transação
        try:
            self.pix_repo.debit(id_conta_origem, valor_decimal)
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
