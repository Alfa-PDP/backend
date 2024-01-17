import logging

from fastapi import FastAPI

from app.core.config import MainConfig
from app.providers.cache_provider import RedisProvider
from app.providers.http_provider import HTTPXClientProvider

logger = logging.getLogger(__name__)


def setup_providers(app: FastAPI, settings: MainConfig) -> None:
    redis_provider = RedisProvider(app=app, host=settings.redis.host, port=settings.redis.port)
    redis_provider.register_events()
    logger.info(f"Setup Redis Provider. host:port: {settings.redis.host}:{settings.redis.port}")

    http_client = HTTPXClientProvider(app=app)
    http_client.register_events()
    logger.info(f"Setup Http Provider. {http_client}")
