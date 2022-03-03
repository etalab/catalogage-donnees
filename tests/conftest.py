import asyncio
import os
from typing import AsyncIterator, Iterator

import httpx
import pytest
from alembic import command
from alembic.config import Config
from asgi_lifespan import LifespanManager
from sqlalchemy_utils import create_database, database_exists, drop_database

from server.config import Settings
from server.config.di import bootstrap, resolve

from .helpers import TestUser, temp_user

os.environ["APP_TESTING"] = "True"

bootstrap()


@pytest.fixture(autouse=True, scope="session")
def test_database() -> Iterator[None]:
    settings = resolve(Settings)

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
    from server.api.app import create_app

    app = create_app()

    async with LifespanManager(app):
        async with httpx.AsyncClient(app=app, base_url="http://testserver") as client:
            yield client


@pytest.fixture(name="temp_user")
async def fixture_temp_user() -> AsyncIterator[TestUser]:
    async with temp_user() as user:
        yield user
