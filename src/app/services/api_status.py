from dataclasses import dataclass

from app.clients.cache.abstract import CacheClientABC
from app.schemas.api_status import APIStatusSchema


@dataclass
class APIStatusService:
    cache_client: CacheClientABC

    async def get_api_status(self) -> APIStatusSchema:
        return APIStatusSchema(
            api=True,
            redis=await self.cache_client.ping(),
        )
