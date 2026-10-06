from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


from src.core.database import get_db
from src.core.security import get_current_customer

from src.modules.ledger.repository import LedgerRepository
from src.modules.ledger.schema import ExtratoItemSchema, ResumoContaSchema, ExtratoCompletoSchema
from src.modules.limits.schema import  LimitesResponseSchema, UpdateLimiteSchema
from src.modules.limits.repository import LimitesRepository
from src.modules.limits.service import LimitesService


router = APIRouter(prefix="/limits", tags=["Limits"])

@router.get("/pix", response_model=LimitesResponseSchema, status_code=status.HTTP_200_OK)
async def consultar_limites_pix(
    id_conta: int = Depends(get_current_customer),
    db: AsyncSession = Depends(get_db)
):
    service = LimitesService(LimitesRepository(db), LedgerRepository(db))
    return await service.obter_status_limites(id_conta)

@router.patch("/pix", response_model=LimitesResponseSchema, status_code=status.HTTP_200_OK)
async def alterar_limites_pix(
    payload: UpdateLimiteSchema,
    id_conta: int = Depends(get_current_customer),
    db: AsyncSession = Depends(get_db)
):
    """
    Atualiza parcialmente os limites operacionais Pix da conta autenticada.
    """
    service = LimitesService(LimitesRepository(db), LedgerRepository(db))
    return await service.atualizar_limites(id_conta, payload)