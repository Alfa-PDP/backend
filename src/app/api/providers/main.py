import logging

from fastapi import FastAPI

from app.api.providers.cache_provider import RedisProvider
from app.api.providers.http_provider import HTTPXClientProvider
from app.api.providers.pg_provider import PostgresqlProvider
from app.core.config import MainConfig

logger = logging.getLogger(__name__)


def setup_providers(app: FastAPI, config: MainConfig) -> None:
    redis_provider = RedisProvider(app=app, host=config.redis.host, port=config.redis.port)
    redis_provider.register_events()
    logger.info(f"Setup Redis Provider. host:port: {config.redis.host}:{config.redis.port}")

    http_client = HTTPXClientProvider(app=app)
    http_client.register_events()
    logger.info(f"Setup Http Provider. {http_client}")

    pg_provider = PostgresqlProvider(app=app, config=config.postgresql)
    pg_provider.register_events()
    logger.info(f"Setup PG Provider. host:port: {config.postgresql.host}: {config.postgresql.port}")
