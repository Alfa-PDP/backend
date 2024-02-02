from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from database.config import PostgresqlConfig

config = PostgresqlConfig()

async_engine = create_async_engine(
    config.database_url,
    echo=True,
    max_overflow=20,
    pool_size=10,
)
async_session_maker = async_sessionmaker(
    async_engine,
    expire_on_commit=False,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
)


@asynccontextmanager
async def db_session(session_maker: async_sessionmaker) -> AsyncGenerator[AsyncSession, None]:
    session: AsyncSession = session_maker()
    try:
        yield session
        await session.commit()
    finally:
        await session.close()
