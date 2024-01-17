from typing import Annotated, AsyncGenerator

from fastapi import Depends, FastAPI, Request
from httpx import AsyncClient
from redis.asyncio import Redis

from app.clients.cache.abstract import CacheClientABC
from app.clients.cache.redis import RedisCacheClient


async def get_httpx_client(request: Request) -> AsyncGenerator[AsyncClient, None]:
    app: FastAPI = request.app
    http_client: AsyncClient = app.state.async_http_client
    yield http_client


async def get_redis_client(request: Request) -> AsyncGenerator[CacheClientABC, None]:
    app: FastAPI = request.app
    redis_client: Redis = app.state.async_redis_client
    try:
        yield RedisCacheClient(redis_client)
    finally:
        await redis_client.close()


CacheClient = Annotated[CacheClientABC, Depends(get_redis_client)]
