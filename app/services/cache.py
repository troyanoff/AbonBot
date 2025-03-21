import orjson

from functools import lru_cache
from redis.asyncio import Redis
from typing import Any

from core.config import settings
from db.redis import get_redis


class Cache:

    def __init__(self, redis: Redis):
        self.redis = redis

    async def get(self, prefix: str, key: str | int) -> Any:
        full_key = f'{prefix}:{key}'
        value = await self.redis.get(full_key)
        if not value:
            return None
        value = orjson.loads(value.decode('utf-8'))
        return value

    async def set(
        self,
        prefix: str,
        key: str | int,
        value: Any,
        ttl: int = settings.default_cache_ttl
    ) -> None:
        full_key = f'{prefix}:{key}'
        json_value = orjson.dumps(value)
        await self.redis.set(full_key, json_value, ttl)

    async def delete(
        self,
        prefix: str,
        key: str | int
    ) -> None:
        full_key = f'{prefix}:{key}'
        await self.redis.delete(full_key)

    async def exists(self, prefix: str, key: str) -> int:
        full_key = f'{prefix}:{key}'
        result = await self.redis.exists(full_key)
        return result


@lru_cache()
def get_cache_service() -> Cache:
    redis = get_redis()
    return Cache(redis)
