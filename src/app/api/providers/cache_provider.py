from fastapi import FastAPI
from redis.asyncio import Redis

from app.api.providers.mixins import ShutDownProviderMixin, StartUpProviderMixin
from app.core.errors import ApplicationError


class RedisProvider(StartUpProviderMixin, ShutDownProviderMixin):
    def __init__(self, app: FastAPI, host: str, port: int):
        self.app = app
        self.host = host
        self.port = port

    async def startup(self) -> None:
        """FastAPI startup event"""

        self.redis_client: Redis = Redis(host=self.host, port=self.port)

        if not await self.redis_client.ping():
            raise ApplicationError()

        setattr(self.app.state, "async_redis_client", self.redis_client)

    async def shutdown(self) -> None:
        """FastAPI shutdown event"""

        if self.redis_client:
            await self.redis_client.close()
