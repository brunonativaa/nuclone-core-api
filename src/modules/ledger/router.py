from typing import List
from fastapi import APIRouter, Depends, Query, status, HTTPException
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.security import get_current_user_id
from src.modules.ledger.schema import  TransactionResponseSchema 
from src.modules.ledger.repository import LedgerRepository


router = APIRouter()

# --- ROTAS DE LEDGER (Somente Leitura) ---
@router.get("/ledger/extrato", response_model=List[TransactionResponseSchema], tags=["Ledger"])
def obter_extrato(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    id_conta: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    repo = LedgerRepository(db)
    return repo.get_extrato_by_conta(id_conta=id_conta, limit=limit, offset=offset)

@router.get("/ledger/transacoes/{id_transacao}", response_model=TransactionResponseSchema, tags=["Ledger"])
def obter_transacao(
    id_transacao: int,
    id_conta: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    repo = LedgerRepository(db)
    transacao = repo.get_by_id(id_transacao)
    if not transacao or (transacao.id_conta_origem != id_conta and transacao.id_conta_destino != id_conta):
        raise HTTPException(status_code=404, detail="Transação não encontrada ou acesso negado.")
    return transacao