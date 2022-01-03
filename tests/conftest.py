import asyncio
import os
from typing import TYPE_CHECKING, AsyncIterator, Iterator

import httpx
import pytest
from alembic import command
from alembic.config import Config
from asgi_lifespan import LifespanManager
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_utils import create_database, database_exists, drop_database

os.environ["APP_TESTING"] = "True"

if TYPE_CHECKING:
    from server.apps.auth import User


@pytest.fixture(autouse=True, scope="session")
def test_database() -> Iterator[None]:
    from server.conf import settings

    url = settings.sync_test_database_url
    assert not database_exists(url), "Test database already exists, aborting tests."

    create_database(url)

    try:
        config = Config("alembic.ini")
        command.upgrade(config, "head")
        yield
    finally:
        drop_database(url)


@pytest.fixture(scope="session")
def event_loop() -> Iterator[asyncio.AbstractEventLoop]:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        yield loop
    finally:
        loop.close()


@pytest.fixture(scope="session")
async def client() -> AsyncIterator[httpx.AsyncClient]:
    from server.app import create_app

    app = create_app()

    async with LifespanManager(app):
        async with httpx.AsyncClient(app=app, base_url="http://testserver") as client:
            yield client


@pytest.fixture(autouse=True)
async def db() -> AsyncIterator[AsyncSession]:
    from server.db import AsyncSessionLocal

    async with AsyncSessionLocal() as db:
        yield db


@pytest.fixture
async def temp_user(db: AsyncSession) -> AsyncIterator["User"]:
    from server.apps.auth import queries as auth_queries

    user = await auth_queries.create_user(db, email="temp@example.org", password="temp")
    try:
        yield user
    finally:
        if await auth_queries.get_user_by_email(db, user.email) is not None:
            await auth_queries.delete_user(db, user)
