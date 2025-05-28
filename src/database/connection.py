from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from loguru import logger
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.config import settings


class Database:
    def __init__(self):
        self.engine: AsyncEngine | None = None
        self.session_factory: async_sessionmaker[AsyncSession] | None = None

    async def connect(self):
        self.engine = create_async_engine(
            url=str(settings.DATABASE.url),
            echo=settings.DATABASE.echo,
            pool_size=20,
            max_overflow=30,
            future=True,
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            expire_on_commit=False,
            class_=AsyncSession
        )
        logger.info("🔌 SQLAlchemy engine created")

    async def disconnect(self):
        if self.engine:
            await self.engine.dispose()
            logger.info("🔌SQLAlchemy engine disposed")

    @asynccontextmanager
    async def session(self) -> AsyncGenerator[AsyncSession, Any]:
        """
        Context manager to automatically close and commit/rollback session.

        Usage:
            async with db.session() as session:
                ...
        """
        if not self.session_factory:
            raise RuntimeError("❌ Session factory is not initialized. Call connect() first.")
        session = self.session_factory()
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()

# Singleton
db = Database()
