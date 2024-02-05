from fastapi import FastAPI
from redis.asyncio import Redis

from app.api.providers.mixins import ShutDownProviderMixin, StartUpProviderMixin
from app.core import errors


class RedisProvider(StartUpProviderMixin, ShutDownProviderMixin):
    def __init__(self, app: FastAPI, host: str, port: int):
        """
        Поставщик Redis для управления событиями запуска и остановки FastAPI.

        Аргументы:
            - app (FastAPI): Экземпляр FastAPI.
            - host (str): Хост Redis.
            - port (int): Порт Redis.
        """
        self.app = app
        self.host = host
        self.port = port

    async def startup(self) -> None:
        """
        Событие запуска FastAPI.

        Создает и проверяет соединение с Redis, затем устанавливает атрибут
            `async_redis_client` в состоянии FastAPI для использования в приложении.
        """
        self.redis_client: Redis = Redis(host=self.host, port=self.port)

        if not await self.redis_client.ping():
            raise errors.ApplicationError

        setattr(self.app.state, "async_redis_client", self.redis_client)

    async def shutdown(self) -> None:
        """
        Событие остановки FastAPI.

        Закрывает соединение с Redis при завершении работы приложения.
        """
        if self.redis_client:
            await self.redis_client.close()
