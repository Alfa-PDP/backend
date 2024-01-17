from abc import ABC, abstractmethod
from dataclasses import dataclass

from app.clients.cache.abstract import CacheClientABC
from app.schemas.status import StatusResponse


class StatusServiceABC(ABC):
    @abstractmethod
    async def get_api_status(self) -> StatusResponse:
        raise NotImplementedError


@dataclass
class StatusService(StatusServiceABC):
    cache_client: CacheClientABC

    async def get_api_status(self) -> StatusResponse:
        return StatusResponse(
            api=True,
            redis=await self.cache_client.ping(),
        )
