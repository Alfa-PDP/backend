from typing import Union

from redis.asyncio import Redis

from app.clients.cache.abstract import CacheClientABC


class RedisCacheClient(CacheClientABC):
    def __init__(self, redis: Redis):
        self.redis = redis

    async def get_from_cache(self, key: str) -> str | None:
        value = await self.redis.get(key)
        if value:
            return value.decode()
        return None

    async def del_from_cache(self, key: str) -> None:
        await self.redis.delete(key)
        return None

    async def put_to_cache(
        self,
        key: str,
        value: Union[str, bytes],
        expire: int,
    ) -> None:
        await self.redis.set(key, value, expire)

    async def increment(self, key: str, amount: int = 1) -> int:
        return await self.redis.incr(key, amount=amount)

    async def set_expire(self, key: str, expire: int = 1) -> int:
        return await self.redis.expire(key, expire)

    async def ping(self) -> bool:
        return await self.redis.ping()
