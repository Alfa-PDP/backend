from abc import ABC, abstractmethod
from dataclasses import dataclass

from app.clients.cache.abstract import CacheClientABC
from app.schemas.status import StatusSchema


@dataclass
class StatusService:
    cache_client: CacheClientABC

    async def get_api_status(self) -> StatusSchema:
        return StatusSchema(
            api=True,
            redis=await self.cache_client.ping(),
        )
