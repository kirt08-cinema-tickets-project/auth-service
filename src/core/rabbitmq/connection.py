import aio_pika


class RabbitMQConnection:
    def __init__(self, url: str):
        self._url = url
        self._connection: aio_pika.RobustConnection | None = None

    async def connect(self):
        if not self._connection:
            self._connection = await aio_pika.connect_robust(
                url = self._url
            )
        
    async def get_channel(self):
        if not self._connection:
            await self.connect()
        return await self._connection.channel()
    
    async def close(self):
        if self._connection:
            await self._connection.close()