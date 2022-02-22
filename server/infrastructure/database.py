from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from .adapters import json

Base = declarative_base()


class Database:
    def __init__(self, url: str, debug: bool = False) -> None:
        self._engine = create_async_engine(url, echo=debug, json_serializer=json.dumps)
        self._session_cls = sessionmaker(
            self._engine, autocommit=False, autoflush=False, class_=AsyncSession
        )

    def session(self) -> AsyncSession:
        return self._session_cls()
