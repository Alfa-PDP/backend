from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.api.providers.mixins import ShutDownProviderMixin, StartUpProviderMixin
from app.core.config import PostgresqlConfig


class PostgresqlProvider(StartUpProviderMixin, ShutDownProviderMixin):
    def __init__(self, app: FastAPI, config: PostgresqlConfig):
        self.app = app
        self.config = config

    async def startup(self) -> None:
        """FastAPI startup event"""

        self.async_engine = create_async_engine(
            self.config.database_url,
            echo=self.config.echo,
            max_overflow=20,
            pool_size=10,
        )
        self.async_session_maker = async_sessionmaker(
            self.async_engine,
            expire_on_commit=False,
            class_=AsyncSession,
            autocommit=False,
            autoflush=False,
        )

        setattr(self.app.state, "async_engine", self.async_engine)
        setattr(self.app.state, "async_session_maker", self.async_session_maker)

    async def shutdown(self) -> None:
        """FastAPI shutdown event"""
        await self.async_engine.dispose()
