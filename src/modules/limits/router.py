from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


from src.core.database import get_db
from src.core.security import get_current_customer

from src.modules.customer.model import ClienteModel
from src.modules.account.model import ContaModel
from src.modules.customer.repository import ClienteRepository
from src.modules.account.repository import ContaRepository
from src.modules.ledger.repository import LedgerRepository
from src.modules.ledger.exceptions import TransacaoNaoEncontradaException
from src.modules.ledger.schema import ExtratoItemSchema, ResumoContaSchema, ExtratoCompletoSchema
from src.modules.limits.schema import  LimitesResponseSchema, UpdateLimiteSchema
from src.modules.limits.repository import LimitesRepository
from src.modules.limits.service import LimitesService


router = APIRouter(prefix="/limits", tags=["Limits"])

@router.get("/pix", response_model=LimitesResponseSchema, status_code=status.HTTP_200_OK)
async def consultar_limites_pix(
    cliente: ClienteModel = Depends(get_current_customer), # 👈 Recebe o Cliente autenticado
    db: AsyncSession = Depends(get_db)
):
    # 1. Busca a conta vinculada ao cliente logado
    conta_repo = ContaRepository(db)
    conta = await conta_repo.get_account_by_id(cliente.id_cliente)
    if not conta:
        raise HTTPException(status_code=404, detail="Conta não encontrada para este cliente.")

    # 2. Executa o serviço utilizando o id_conta real (int)
    service = LimitesService(LimitesRepository(db), LedgerRepository(db))
    return await service.obter_status_limites(conta.id_conta)


@router.patch("/pix", response_model=LimitesResponseSchema, status_code=status.HTTP_200_OK)
async def alterar_limites_pix(
    payload: UpdateLimiteSchema,
    cliente: ClienteModel = Depends(get_current_customer), # 👈 Recebe o Cliente autenticado
    db: AsyncSession = Depends(get_db)
):
    conta_repo = ContaRepository(db)
    conta = await conta_repo.get_account_by_id(cliente.id_cliente)
    if not conta:
        raise HTTPException(status_code=404, detail="Conta não encontrada para este cliente.")

    service = LimitesService(LimitesRepository(db), LedgerRepository(db))
    return await service.atualizar_limites(conta.id_conta, payload)

@router.get("/transacoes/{id_transacao}", response_model=ExtratoItemSchema)
async def get_transacao_por_id(
    id_transacao: int,
    conta: ContaModel = Depends(get_current_customer),
    db: AsyncSession = Depends(get_db)
):
    service = LedgerService(LedgerRepository(db))
    try:
        transacao = await service.get_by_id(id_transacao)
        
        # Blindagem de IDOR: garante que a transação pertence à conta autenticada
        if transacao.id_conta_origem != conta.id_conta and transacao.id_conta_destino != conta.id_conta:
            raise TransacaoNaoEncontradaException(id_transacao)
            
        return transacao
        
    except TransacaoNaoEncontradaException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "code": "TRANSACTION_NOT_FOUND",
                "message": str(e)
            }
        )