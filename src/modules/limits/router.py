from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.security import get_current_user_id

from src.modules.ledger.repository import LedgerRepository
from src.modules.limits.schema import  LimitesResponseSchema, UpdateLimiteSchema
from src.modules.limits.repository import LimitesRepository
from src.modules.limits.service import LimitesService


router = APIRouter(prefix="/limits", tags=["Limits"])

@router.get("/pix", response_model=LimitesResponseSchema, status_code=status.HTTP_200_OK)
def consultar_limites_pix(
    id_conta: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    service = LimitesService(LimitesRepository(db), LedgerRepository(db))
    return service.obter_status_limites(id_conta)

@router.patch("/pix", response_model=LimitesResponseSchema, status_code=status.HTTP_200_OK)
def alterar_limites_pix(
    payload: UpdateLimiteSchema,
    id_conta: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    Atualiza parcialmente os limites operacionais Pix da conta autenticada.
    """
    service = LimitesService(LimitesRepository(db), LedgerRepository(db))
    return service.atualizar_limites(id_conta, payload)