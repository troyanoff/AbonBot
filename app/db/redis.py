from redis.asyncio import Redis

redis: Redis | None = None


def get_redis() -> Redis:
    return redis
