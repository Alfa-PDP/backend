from abc import ABC, abstractmethod
from typing import Any, Optional


class AsyncHTTPClientABC(ABC):
    @abstractmethod
    async def get(
        self,
        path: str,
        params: Optional[dict] = None,
        headers: Optional[dict] = None,
    ) -> Any:
        raise NotImplementedError

    @abstractmethod
    async def post(
        self,
        path: str,
        headers: Optional[dict] = None,
        data: Optional[dict] = None,
        params: Optional[dict] = None,
    ) -> Any:
        raise NotImplementedError
