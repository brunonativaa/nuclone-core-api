from datetime import datetime, timezone, timedelta
from decimal import Decimal
from zoneinfo import ZoneInfo
from src.modules.ledger.repository import LedgerRepository

class LedgerService:
    def __init__(self, ledger_repo: LedgerRepository):
        self.ledger_repo = ledger_repo
        self.tz_br = ZoneInfo("America/Sao_Paulo")

    def is_horario_noturno(self, data_hora: datetime) -> bool:
        """Determina se a transação ocorre na janela noturna (20h às 06h)."""
        hora_local = data_hora.astimezone(self.tz_br).hour
        return hora_local >= 20 or hora_local < 6

    async def obter_extrato(self, id_conta: int, limit: int, offset: int):
        # Aqui podemos injetar regras de mascaramento de dados ou auditoria se necessário
        return await self.ledger_repo.get_extrato_by_conta(id_conta, limit, offset)