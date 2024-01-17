from app.deps.clients import CacheClient
from app.services.status import StatusService, StatusServiceABC


def create_status_service(cache_client: CacheClient) -> StatusServiceABC:
    return StatusService(cache_client)
