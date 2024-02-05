from typing import Annotated, AsyncGenerator

from fastapi import Depends, FastAPI, Request
from httpx import AsyncClient
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.clients.cache.abstract import CacheClientABC
from app.clients.cache.redis import RedisCacheClient
from app.clients.http.abstract import AsyncHTTPClientABC
from app.clients.http.http_client import AsyncHTTPClient


async def get_httpx_client(request: Request) -> AsyncGenerator[AsyncHTTPClientABC, None]:
    """
    Получает асинхронного HTTP-клиента из состояния FastAPI.

    Аргументы:
        - request: Экземпляр Request, предоставленный FastAPI.

    Возвращает:
        - AsyncGenerator[AsyncHTTPClientABC, None]: Асинхронный генератор для HTTP-клиента.
    """
    app: FastAPI = request.app
    http_client: AsyncClient = app.state.async_http_client
    yield AsyncHTTPClient(http_client)


HttpxClientDep = Annotated[AsyncClient, Depends(get_httpx_client)]


async def get_redis_client(request: Request) -> AsyncGenerator[CacheClientABC, None]:
    """
    Получает асинхронного клиента кэша Redis из состояния FastAPI.

    Аргументы:
        - request: Экземпляр Request, предоставленный FastAPI.

    Возвращает:
        - AsyncGenerator[CacheClientABC, None]: Асинхронный генератор для клиента кэша Redis.
    """
    app: FastAPI = request.app
    redis_client: Redis = app.state.async_redis_client
    try:
        yield RedisCacheClient(redis_client)
    finally:
        await redis_client.close()


CacheClientDep = Annotated[CacheClientABC, Depends(get_redis_client)]


async def get_db_session(
    request: Request,
) -> AsyncGenerator[AsyncSession, None]:
    """
    Получает асинхронную сессию базы данных из состояния FastAPI.

    Аргументы:
        - request: Экземпляр Request, предоставленный FastAPI.

    Возвращает:
        - AsyncGenerator[AsyncSession, None]: Асинхронный генератор для асинхронной сессии базы данных.
    """
    app: FastAPI = request.app
    session_maker = app.state.async_session_maker
    session: AsyncSession = session_maker()
    try:
        yield session
    finally:
        await session.commit()
        await session.close()


DbSessionDep = Annotated[AsyncSession, Depends(get_db_session)]
