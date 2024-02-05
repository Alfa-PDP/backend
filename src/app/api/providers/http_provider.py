from typing import Optional

from fastapi import FastAPI
from httpx import AsyncClient

from app.api.providers.mixins import StartUpProviderMixin


class HTTPXClientProvider(StartUpProviderMixin):
    def __init__(self, app: FastAPI):
        """
        Поставщик HTTPX-клиента для управления событием запуска FastAPI.

        Аргументы:
            - app (FastAPI): Экземпляр FastAPI.
        """
        self.app = app
        self.http_client: Optional[AsyncClient] = None

    async def startup(self) -> None:
        """
        Событие запуска FastAPI.

        Создает асинхронного HTTPX-клиента и устанавливает его в состоянии FastAPI
            для использования в приложении.
        """
        self.http_client = AsyncClient()
        setattr(self.app.state, "async_http_client", self.http_client)
