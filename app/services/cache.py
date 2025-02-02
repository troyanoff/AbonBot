import orjson

from functools import lru_cache
from typing import Any

from core.config import settings
from services.storage import RedisService, get_redis_service

class Cache:
    
    def __init__(self, storage: RedisService):
        self.storage = storage

    async def get(self, prefix: str, key: str | int) -> Any:
        full_key = f'{prefix}:{key}'
        value = await self.storage.get(full_key)
        if not value:
            return None
        value = orjson.loads(value)
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
        await self.storage.set(full_key, json_value, ttl)

    async def delete(
        self,
        prefix: str,
        key: str | int
    ):
        full_key = f'{prefix}:{key}'
        await self.storage.delete(full_key)


@lru_cache()
def get_cache_service() -> Cache:
    storage = get_redis_service()
    return Cache(storage)
