from unittest.mock import AsyncMock

import pytest

from app.schemas.status import StatusSchema
from app.services.status import StatusService


@pytest.mark.asyncio
async def test_status_service() -> None:
    cache_mock = AsyncMock()
    cache_mock.ping.return_value = True

    service = StatusService(cache_mock)
    result = await service.get_api_status()

    cache_mock.ping.assert_called_with()
    assert isinstance(result, StatusSchema)
    assert result.api is True
    assert result.redis is True
