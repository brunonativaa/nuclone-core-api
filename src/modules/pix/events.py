import uuid
from decimal import Decimal
from typing import Dict, Any
from src.core.broker import RabbitMQBroker


class PixEventOperations:
    async def disparar_pix_solicitado(
        self,
        id_transacao: int,
        id_conta_origem: int,
        id_conta_destino: int,
        valor: Decimal
    ) -> None:

        payload: Dict[str, Any] = {
            "event_id": str(uuid.uuid4()),
            "id_transacao": id_transacao,
            "id_conta_origem": id_conta_origem,
            "id_conta_destino": id_conta_destino,
            "valor": str(valor),
            "status": "PROCESSANDO"
        }

        broker = RabbitMQBroker()

        await broker.publish_event(
            exchange_name="nuclone.pix.exchange",
            routing_key="pix.solicitado",
            payload=payload
        )