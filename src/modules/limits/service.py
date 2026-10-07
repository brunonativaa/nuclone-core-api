from datetime import datetime, timezone, timedelta
from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
import zoneinfo 
from src.modules.limits.schema import UpdateLimiteSchema
from src.modules.limits.repository import LimitesRepository
from src.modules.ledger.repository import LedgerRepository
from src.modules.limits.exceptions import LimitNotFoundException, ExceededLimitException

class LimitesService:
    def __init__(self, limits_repo: LimitesRepository, ledger_repo: LedgerRepository):
        self.limits_repo = limits_repo
        self.ledger_repo = ledger_repo
        self.tz_br = zoneinfo.ZoneInfo("America/Sao_Paulo")
    
    def _is_horario_noturno(self, data_hora: datetime) -> bool: 
            """Determina se a transação ocorre na janela noturna (20h às 06h BRT).
            
            Método síncrono utilitário (CPU-bound puro).
            """
            hora_local = data_hora.astimezone(self.tz_br).hour
            return hora_local >= 20 or hora_local < 6
        

    async def validar_e_consumir_limite(self, id_conta: int, valor: Decimal) -> bool:
        limite_config = await self.limits_repo.get_by_conta(id_conta)
        if not limite_config:
            raise LimitNotFoundException("Configuração de limites não encontrada.")

        agora = datetime.now(timezone.utc)
        is_noturno =  self._is_horario_noturno(agora)
        limite_maximo = limite_config.limite_noturno if is_noturno else limite_config.limite_diario

        inicio_janela = agora - timedelta(hours=24)

        gasto_atual = await self.ledger_repo.get_total_gasto_janela(
            id_conta=id_conta,
            inicio=inicio_janela,
            fim=agora,
            is_noturno=is_noturno
        )

        disponivel = limite_maximo - gasto_atual

        if (gasto_atual + valor) > limite_maximo:
            periodo = "noturno" if is_noturno else "diario"
            raise ExceededLimitException(
                message=f"Transação excede o limite {periodo} disponível. Disponível: R$ {disponivel:.2f}",
                disponivel=disponivel   
            )

        return True

    async def obter_status_limites(self, id_conta: int) -> dict:
        limite_config = await self.limits_repo.get_by_conta(id_conta)
        if not limite_config:
            raise LimitNotFoundException("Configuração de limites não encontrada para esta conta.")

        agora = datetime.now(timezone.utc)
        inicio_janela = agora - timedelta(hours=24)

        gasto_diario = await self.ledger_repo.get_total_gasto_janela(
            id_conta=id_conta,
            inicio =inicio_janela,
            fim=agora,
            is_noturno=False,
            )
        
        gasto_noturno = await self.ledger_repo.get_total_gasto_janela(
            id_conta=id_conta,
            inicio=inicio_janela,
            fim=agora,
            is_noturno=True,
        )

        return {
            "id_conta": id_conta,
            "limite_diario": limite_config.limite_diario,
            "limite_noturno": limite_config.limite_noturno,
            "limite_diario_utilizado": gasto_diario,
            "limite_noturno_utilizado": gasto_noturno
        }

    async def atualizar_limites(self, id_conta: int, payload: UpdateLimiteSchema) -> dict:
        limite_config = await self.limits_repo.get_by_conta(id_conta)
        if not limite_config:
            raise LimitNotFoundException(
                "Configuração de limites não encontrada para esta conta."
            )

        if payload.novo_limite_diario is not None:
            limite_config.limite_diario = payload.novo_limite_diario

        if payload.novo_limite_noturno is not None:
            limite_config.limite_noturno = payload.novo_limite_noturno

        await self.limits_repo.update_limits(limite_config)
        return await self.obter_status_limites(id_conta)