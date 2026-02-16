import aio_pika

from src.core.rabbitmq.connection import RabbitMQConnection


class RabbitMQPublisher:
    def __init__(self, connection: RabbitMQConnection):
        self._connection = connection
        self._channel: aio_pika.RobustChannel | None = None

    async def start(self):
        self._channel = await self._connection.get_channel()

        await self._channel.set_qos(prefetch_count=1)


    async def publish(self, queue_name: str, message: str):
        if not self._channel:
            await self.start()

        body = message.encode()

        await self._channel.default_exchange.publish(
            aio_pika.Message(body=body),
            routing_key=queue_name,
        )

