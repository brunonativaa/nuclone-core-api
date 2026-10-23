from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.core.broker import RabbitMQBroker


@pytest.mark.asyncio
async def test_publish_event_success():
    # Canal e exchange
    mock_channel = AsyncMock()
    mock_exchange = AsyncMock()

    mock_channel.declare_exchange.return_value = mock_exchange

    # Context manager do channel()
    mock_channel_context = AsyncMock()
    mock_channel_context.__aenter__.return_value = mock_channel
    mock_channel_context.__aexit__.return_value = None

    # Connection
    mock_connection = MagicMock()
    mock_connection.channel.return_value = mock_channel_context

    with patch("aio_pika.connect_robust", new_callable=AsyncMock) as mock_connect:
        mock_connect.return_value = mock_connection

        broker = RabbitMQBroker()

        payload = {
            "event_id": "uuid-teste",
            "id_transacao": 1,
            "id_conta_origem": 10,
            "id_conta_destino": 20,
            "valor": "100.0",
            "status": "PROCESSANDO"
        }

        await broker.publish_event(
            "nuclone.pix.exchange",
            "pix.solicitado",
            payload
        )

        # conexão criada
        mock_connect.assert_awaited_once()

        # exchange declarada
        mock_channel.declare_exchange.assert_awaited_once()

        # publicação realizada
        mock_exchange.publish.assert_awaited_once()