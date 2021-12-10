from typing import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .conf import settings

database_url = settings.test_database_url if settings.testing else settings.database_url

engine = create_async_engine(database_url, echo=True)
AsyncSessionLocal = sessionmaker(
    engine, autocommit=False, autoflush=False, class_=AsyncSession
)

Base = declarative_base()


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db() -> AsyncIterator[AsyncSession]:
    async with AsyncSessionLocal() as session:
        yield session
