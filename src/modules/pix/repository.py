from decimal import Decimal
from typing import Optional
from sqlalchemy import or_
from sqlalchemy.orm import Session
from src.modules.account.model import ContaModel,  SaldoContaModel
from src.modules.customer.model import ClienteModel, TelefoneModel
from src.modules.ledger.model import TransacaoModel, TipoTransacaoEnum
from src.modules.pix.model import ChavePixModel


class PixRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_key_by_value(self, valor_chave: str) -> Optional[ChavePixModel]:
        """Busca uma chave PIX específica pelo seu valor."""
        return (
            self.db.query(ChavePixModel)
            .filter(ChavePixModel.valor_chave == valor_chave)
            .first()
        )

    def create_pix_key(self, id_conta: int, tipo_chave: str, valor_chave: str) -> ChavePixModel:
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
        self.db.flush()  # Flush para obter o ID da chave PIX gerada
        return nova_chave

    

    def search_account_by_key(self, chave_pix: str) -> Optional[ContaModel]:
        """Busca a conta associada a uma chave PIX, CPF, e-mail ou telefone."""
        return (
            self.db.query(ContaModel)
            .join(ChavePixModel, ContaModel.id_conta == ChavePixModel.id_conta)
            .join(ClienteModel, ContaModel.id_cliente == ClienteModel.id_cliente)
            .outerjoin(TelefoneModel, ClienteModel.id_cliente == TelefoneModel.id_cliente)
            .filter(
                or_(
                    ChavePixModel.valor_chave == chave_pix,
                    ClienteModel.cpf == chave_pix,
                    ClienteModel.email == chave_pix,
                    TelefoneModel.numero == chave_pix
                )
            )
            .first()
        )

    def update_saldo(self, id_conta, valor):
        saldo = self.db.query(SaldoContaModel).filter_by(
            id_conta=id_conta).first()

        if not saldo:
            return None

        saldo.saldo_disponivel += Decimal(str(valor))

        self.db.add(saldo)
        return saldo

    def debit_with_lock(self, id_conta: int, valor: Decimal) -> bool:
        """
        Aplica Pessimistic Locking (FOR UPDATE) para evitar race conditions
        e garante que o saldo seja suficiente antes de debitar.
        """
        saldo = (
            self.db.query(SaldoContaModel)
            .filter_by(id_conta=id_conta)
            .with_for_update()  # Bloqueia a linha para esta transação
            .first()
        )

        if not saldo or saldo.saldo_disponivel < valor:
            return False    

        saldo.saldo_disponivel -= valor
        self.db.add(saldo)
        return True

    def credit(self, id_conta, valor):
        # Passa o valor positivo para somar
        return self.update_saldo(id_conta, Decimal(str(valor)))

    def record_transaction(self, data: dict):
        transacao = TransacaoModel(
            id_conta_origem=data["id_conta_origem"],
            id_conta_destino=data["id_conta_destino"],
            tipo_transacao=data["tipo_transacao"],
            valor=data["valor"]
        )
        self.db.add(transacao)
        self.db.flush()

        return transacao
