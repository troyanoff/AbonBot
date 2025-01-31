
from functools import lru_cache
from redis.asyncio import Redis

from core.config import settings
from db.redis import get_redis


class RedisService:

    def __init__(self, redis: Redis):
        self.redis = redis

    async def get(self, key: str):
        value = await self.redis.get(key)
        if not value:
            return None
        value = value.decode('utf-8')
        return value

    async def set(self, key: str, value: str | int, seconds: int):
        await self.redis.set(key, value, seconds)



@lru_cache()
def get_redis_service() -> RedisService:
    redis = get_redis()
    return RedisService(redis)
