from unittest.mock import AsyncMock

import pytest
from pydantic_core import ValidationError

from app.clients.cache.abstract import CacheClientABC
from app.schemas.api_status import APIStatusSchema
from app.services.api_status import APIStatusService


@pytest.mark.asyncio
@pytest.mark.parametrize("expected", [APIStatusSchema(api=True, redis=True)])
async def test_status_service(expected: APIStatusSchema) -> None:
    cache_mock = AsyncMock(spec=CacheClientABC)
    cache_mock.ping.return_value = True

    service = APIStatusService(cache_mock)
    result = await service.get_api_status()

    cache_mock.ping.assert_called_with()
    assert result == expected


@pytest.mark.asyncio
async def test_status_service_cache_fail() -> None:
    cache_mock = AsyncMock(spec=CacheClientABC)
    cache_mock.ping.return_value = 123

    service = APIStatusService(cache_mock)

    with pytest.raises(ValidationError):
        await service.get_api_status()
