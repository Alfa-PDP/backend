from unittest.mock import AsyncMock

import pytest
from pydantic_core import ValidationError

from app.clients.cache.abstract import CacheClientABC
from app.schemas.status import StatusSchema
from app.services.status import StatusService


@pytest.mark.asyncio
@pytest.mark.parametrize("expected", [StatusSchema(api=True, redis=True)])
async def test_status_service(expected: StatusSchema) -> None:
    cache_mock = AsyncMock(spec=CacheClientABC)
    cache_mock.ping.return_value = True

    service = StatusService(cache_mock)
    result = await service.get_api_status()

    cache_mock.ping.assert_called_with()
    assert result == expected


@pytest.mark.asyncio
async def test_status_service_cache_fail() -> None:
    cache_mock = AsyncMock(spec=CacheClientABC)
    cache_mock.ping.return_value = 123

    service = StatusService(cache_mock)

    with pytest.raises(ValidationError):
        await service.get_api_status()
