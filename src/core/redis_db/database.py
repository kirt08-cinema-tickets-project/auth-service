from functools import lru_cache
import redis.asyncio as redis

from src.core.config import settings

@lru_cache
def get_redis_client() -> redis.Redis:
    pool = redis.ConnectionPool(
        host=settings.redis_db.host,
        port=settings.redis_db.port,
        db=settings.redis_db.db,
        password=settings.redis_db.password.get_secret_value(),
        max_connections=20,
        socket_timeout=2,
        socket_connect_timeout=2,
        retry_on_timeout=True,
    )

    return redis.Redis(
        connection_pool=pool,
        decode_responses=True,
    )

class RedisService:
    def __init__(self, client : redis.Redis):
        self._client = client

    async def get(self, key : str) -> str | None:
        return await self._client.get(key)
    
    async def set(self, key : str, value, ex : int | None = None):
        return await self._client.set(key, value, ex = ex)
    
    async def delete(self, key : str) -> bool:
        return bool(await self._client.delete(key))
    
async def get_redis() -> RedisService:
    client = get_redis_client()
    return RedisService(client)