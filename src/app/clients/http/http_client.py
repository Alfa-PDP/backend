import logging
from typing import Any, Optional

from httpx import AsyncClient, codes

from app.clients.http.abstract import AsyncHTTPClientABC
from app.clients.http.errors import HttpClientError

logger = logging.getLogger(__name__).getChild("http_client")


class AsyncHTTPClient(AsyncHTTPClientABC):
    def __init__(self, httpx_client: AsyncClient):
        self.httpx_client = httpx_client

    async def _request(
        self,
        method: str,
        url: str,
        headers: Optional[dict] = None,
        params: Optional[dict] = None,
        data: Optional[dict] = None,
    ) -> Any:
        response = await self.httpx_client.request(
            method,
            url,
            headers=headers,
            params=params,
            data=data,
        )
        if response.status_code != codes.OK:
            raise HttpClientError(f"Error send post request. detail={response.content!r}")
        return response.json()

    async def get(
        self,
        path: str,
        params: Optional[dict] = None,
        headers: Optional[dict] = None,
    ) -> Any:
        return await self._request(
            method="GET",
            url=path,
            headers=headers,
            params=params,
        )

    async def post(
        self,
        path: str,
        headers: Optional[dict] = None,
        data: Optional[dict] = None,
        params: Optional[dict] = None,
    ) -> Any:
        return await self._request(
            method="POST",
            url=path,
            headers=headers,
            data=data,
            params=params,
        )
