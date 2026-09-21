from typing import List
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.core.security import get_current_user_id

from src.modules.ledger.repository import LedgerRepository
from src.modules.limits.schema import  LimitsResponseSchema, UpdateLimiteSchema
from src.modules.limits.repository import LimitsRepository
from src.modules.limits.service import LimitsService


router = APIRouter()

@router.get("/limits/pix", response_model=LimitsResponseSchema, tags=["Limits"])
def consultar_limites(
    id_conta: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    service = LimitsService(LimitsRepository(db), LedgerRepository(db))
    return service.obter_status_limites(id_conta)

@router.patch("/limits/pix", response_model=LimitsResponseSchema, tags=["Limits"])
def alterar_limites(
    payload: UpdateLimiteSchema,
    id_conta: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)

):
    pass