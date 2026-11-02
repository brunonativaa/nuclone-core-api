import json
import aio_pika
from typing import Any, Dict
from src.core.config import get_settings

class RabbitMQBroker:
    def __init__(self):
        from src.core.config import get_settings
        self.url = get_settings().RABBITMQ_URL
        self._connection = None

    async def connect(self):
        if not self._connection or self._connection.is_closed:
            self._connection = await aio_pika.connect_robust(self.url)

    async def declare_topology(self, exchange_name: str, queue_name: str, routing_key: str):
        await self.connect()

        exchange = await self._connection.channel().declare_exchange(
            exchange_name,
            aio_pika.ExchangeType.TOPIC,
            durable=True
        )

        queue = await self._connection.channel().declare_queue(
            queue_name,
            durable=True
        )
       
        await queue.bind(exchange, routing_key)

    async def publish_event(self, exchange_name: str, routing_key: str, payload: Dict[str, Any]):
        await self.connect()
        
        # O channel() aqui atua como um context manager assíncrono no aio-pika
        async with self._connection.channel() as channel:
            exchange = await channel.declare_exchange(
                exchange_name,
                aio_pika.ExchangeType.TOPIC,
                durable=True
            )

            message = aio_pika.Message(
                body=json.dumps(payload).encode('utf-8'),
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
                content_type="application/json"
            )

            await exchange.publish(message, routing_key=routing_key)

broker = RabbitMQBroker()


