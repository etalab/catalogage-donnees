from contextlib import asynccontextmanager
from typing import AsyncIterator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    AsyncTransaction,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base, sessionmaker

from .adapters import json

Base = declarative_base()


class Database:
    def __init__(self, url: str, debug: bool = False) -> None:
        self._engine = create_async_engine(url, echo=debug, json_serializer=json.dumps)
        self._session_cls = sessionmaker(
            self._engine, autocommit=False, autoflush=False, class_=AsyncSession
        )

    @property
    def engine(self) -> AsyncEngine:
        return self._engine

    def session(self) -> AsyncSession:
        return self._session_cls()

    @asynccontextmanager
    async def transaction(self) -> AsyncIterator[AsyncTransaction]:
        async with self._engine.connect() as conn:
            self._session_cls.configure(bind=conn)
            try:
                async with conn.begin() as tx:
                    yield tx
            finally:
                self._session_cls.configure(bind=self._engine)
