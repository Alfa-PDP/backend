from typing import Optional

from fastapi import FastAPI
from httpx import AsyncClient

from app.api.providers.mixins import StartUpProviderMixin


class HTTPXClientProvider(StartUpProviderMixin):
    def __init__(self, app: FastAPI):
        self.app = app
        self.http_client: Optional[AsyncClient] = None

    async def startup(self) -> None:
        """FastAPI startup event"""
        self.http_client = AsyncClient()
        setattr(self.app.state, "async_http_client", self.http_client)
