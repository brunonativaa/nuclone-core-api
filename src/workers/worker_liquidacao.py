import asyncio
import json
import os
import logging
import sys
from dotenv import load_dotenv
from aio_pika import connect_robust, IncomingMessage
from aio_pika.exceptions import AMQPException

load_dotenv()

logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s [%(levelname)s]%(name)s: %(message)s", 
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("NucloneWorker")

RABBITMQ_URL = os.getenv("RABBITMQ_URL")
RABBITMQ_QUEUE_NAME = os.getenv("RABBITMQ_QUEUE_NAME", "pix.processing_queue")

if not RABBITMQ_URL:
    logger.error("Variável de ambiente RABBITMQ_URL não definida. Encerrando o worker.")
    sys.exit(1)

async def process_message(message: IncomingMessage):
        try:
            body = message.body.decode("utf-8")
            payload = json.loads(body)

            logger.info(f"[x] Processando Pix ID: {payload.get('event_id')}")
            await asycio.sleep(1)  # Simula o processamento do Pix
            logger.info(f"[✔] Liquidação concluida com sucesso!")

        except Exception as e:
            logger.error(f"[!] Erro ao processar a mensagem: {e}")
            await message.nack(requeue=True)  # Reenvia a mensagem para a fila em caso de erro

async def main():
    logger.info("Iniciando o worker de liquidação Pix...")
    connection = await connect_robust(RABBITMQ_URL)

    async with connection:
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=1)
        queue = await channel.declare_queue(RABBITMQ_QUEUE_NAME, durable=True)

    logger.info(f"[*] Escutando a fila '{RABBITMQ_QUEUE_NAME}' para mensagens de liquidação Pix...")
    await queue.consume(process_message)
    await asyncio.Future()  # Mantém o worker em execução


if __name__ == "__main__":
    try: 
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("[*] Worker encerrado com segurança.")