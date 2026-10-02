from typing import List
from fastapi import APIRouter, Depends, Query, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.core.database import get_db
from src.core.security import get_current_customer
from src.modules.ledger.schema import ExtratoItemSchema
from src.modules.ledger.repository import LedgerRepository
from src.modules.customer.model import ClienteModel
from src.modules.account.model import ContaModel

router = APIRouter(prefix="/ledger", tags=["Ledger & Extratos"])


# --- DEPENDÊNCIA AUXILIAR: Recupera a Conta a partir do Cliente Autenticado ---
async def get_current_account(
    current_user: ClienteModel = Depends(get_current_customer),
    db: AsyncSession = Depends(get_db)
) -> ContaModel:
    """
    Garante que o cliente autenticado possui uma conta válida ativa.
    Evita repetição de código (DRY) entre os endpoints do Ledger.
    """
    query = select(ContaModel).where(
        ContaModel.id_cliente == current_user.id_cliente)
    result = await db.execute(query)
    conta = result.scalar_one_or_none()

    if not conta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conta bancária não localizada para o usuário autenticado."
        )
    return conta


# --- ROTAS DE LEDGER (Somente Leitura e Protegidas por JWT) ---

@router.get("/extrato", response_model=List[ExtratoItemSchema])
async def get_bank_extract(
    limit: int = Query(
        20, ge=1, le=100, description="Quantidade máxima de registros"),
    offset: int = Query(0, ge=0, description="Página/Offset da paginação"),
    conta: ContaModel = Depends(get_current_account),
    db: AsyncSession = Depends(get_db)
):
    """
    Retorna o extrato de lançamentos no Ledger do cliente autenticado com suporte a paginação.
    """
    repo = LedgerRepository(db)
    return await repo.get_extrato_by_conta(id_conta=conta.id_conta, limit=limit, offset=offset)


@router.get("/transacoes/{id_transacao}", response_model=ExtratoItemSchema)
async def get_transaction(
    id_transacao: int,
    conta: ContaModel = Depends(get_current_account),
    db: AsyncSession = Depends(get_db)
):
    """
    Recupera um lançamento específico do Ledger, validando se pertence à conta do usuário autenticado.
    """
    repo = LedgerRepository(db)
    transacao = await repo.get_by_id(id_transacao)

    # Validação de Segurança (Insecure Direct Object Reference - IDOR):
    # Impede que o Usuário A veja uma transação do Usuário B
    if not transacao or (
        transacao.id_conta_origem != conta.id_conta and
        transacao.id_conta_destino != conta.id_conta
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transação não localizada ou acesso não autorizado."
        )

    return transacao
