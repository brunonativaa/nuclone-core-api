from datetime import datetime, timezone, timedelta
from decimal import Decimal
from fastapi import HTTPException, status
from src.modules.limits.repository import LimitsRepository
from src.modules.ledger.repository import LedgerRepository


class LimitsService:
    def __init__(self, limits_repo: LimitsRepository, ledger_repo: LedgerRepository):
        self.limits_repo = limits_repo
        self.ledger_repo = ledger_repo

    def validar_e_consumir_limite(self, id_conta: int, valor: Decimal) -> bool:
        limite_config = self.limits_repo.get_by_conta(id_conta)
        if not limite_config:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Configuração de limites não encontrada.")

        agora = datetime.now(timezone.utc)
        hora_atual = agora.hour

        is_noturno = hora_atual >= 20 or hora_atual < 6
        limite_maximo = limite_config.limite_noturno if is_noturno else limite_config.limite_diario

        inicio_janela = agora = timedelta(hours=24)
        gasto_atual = self.ledger_repo.get_total_gasto_janela(id_conta, inicio_janela, agora)

        if (gasto_atual + valor) > limite_maximo:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Transação excede o limite {'noturno' if is_noturno else 'diário'} disponível. Disponível: R$ {limite_maximo - gasto_atual:.2f}"
            )
        return True


    def obter_status_limites(self, id_conta: int):
        limite_config = self.limits_repo.get_by_conta(id_conta)
        if not limite_config:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Limites não configurados.")

        agora = datetime.now(timezone.utc)
        inicio_janela = agora - timedelta(hours=24)
        gasto_total = self.ledger_repo.get_total_gasto_janela(id_conta, inicio_janela, agora)

        return {
            "id_conta": id_conta,
            "limite_diario": limite_config.limite_diario,
            "limite_noturno": limite_config.limite_noturno,
            "limite_diario_utilizado": gasto_total,
            "limite_noturno_utilizado": gasto_total
        }
