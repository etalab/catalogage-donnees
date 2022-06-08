from contextlib import asynccontextmanager
from typing import AsyncIterator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    AsyncTransaction,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeMeta, registry, sessionmaker

mapper_registry = registry()


class Base(metaclass=DeclarativeMeta):
    # Explicit SQLAlchemy declarative base, for use with mypy.
    # See: https://docs.sqlalchemy.org/en/20/orm/declarative_styles.html#creating-an-explicit-base-non-dynamically-for-use-with-mypy-similar  # noqa
    # NOTE: as of SQLAlchemy 1.4, the mypy plugin is considered as legacy, but
    # still required for full mypy support. SQLAlchemy 2.0 is planned to include new
    # constructs that allow full mypy support without the plugin.
    # See: https://docs.sqlalchemy.org/en/20/orm/extensions/mypy.html

    __abstract__ = True
    registry = mapper_registry
    metadata = mapper_registry.metadata
    __init__ = mapper_registry.constructor


class Database:
    def __init__(self, url: str, debug: bool = False) -> None:
        self._engine = create_async_engine(url, echo=debug, future=True)
        self._session_cls = sessionmaker(
            bind=self._engine, class_=AsyncSession, future=True
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
