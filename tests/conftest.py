import asyncio
import os
from typing import TYPE_CHECKING, AsyncIterator, Iterator, List

import httpx
import pytest
import pytest_asyncio
from alembic import command
from alembic.config import Config
from asgi_lifespan import LifespanManager
from sqlalchemy_utils import create_database, database_exists, drop_database

from server.application.datasets.queries import GetAllDatasets
from server.application.tags.queries import GetAllTags
from server.application.tags.views import TagView
from server.config import Settings
from server.config.di import bootstrap, resolve
from server.domain.auth.entities import UserRole
from server.infrastructure.database import Database
from server.seedwork.application.messages import MessageBus
from tests.factories import CreateTagFactory

from .helpers import TestUser, create_client, create_test_user

if TYPE_CHECKING:
    from server.api.app import App

os.environ["APP_TESTING"] = "True"
os.environ["APP_SANDBOX_CONFIG_API_KEY"] = "<testing>"

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


@pytest_asyncio.fixture(autouse=True)
async def autorollback_db() -> AsyncIterator[None]:
    db = resolve(Database)

    async with db.autorollback():
        yield


@pytest_asyncio.fixture(scope="session", autouse=True)
async def warmup_db() -> None:
    # Run a database query to warmup tables. Otherwise this warmup would
    # occur during tests and interfere with time measurements.
    bus = resolve(MessageBus)
    await bus.execute(GetAllDatasets())


@pytest_asyncio.fixture
async def tags() -> List[TagView]:
    bus = resolve(MessageBus)

    for name in [
        "Monument historique",
        "Lieu culturel",
        "Musée de France",
        "Statistiques",
    ]:
        await bus.execute(CreateTagFactory.build(name=name))

    return await bus.execute(GetAllTags())


@pytest.fixture(scope="session")
def event_loop() -> Iterator[asyncio.AbstractEventLoop]:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        yield loop
    finally:
        loop.close()


@pytest_asyncio.fixture(scope="session")
async def app() -> AsyncIterator["App"]:
    from server.api.app import create_app

    app = create_app()

    async with LifespanManager(app):
        yield app


@pytest_asyncio.fixture(scope="session")
async def client(app: "App") -> AsyncIterator[httpx.AsyncClient]:
    async with create_client(app) as client:
        yield client


@pytest_asyncio.fixture(name="temp_user")
async def fixture_temp_user() -> TestUser:
    return await create_test_user(UserRole.USER)


@pytest_asyncio.fixture
async def admin_user() -> TestUser:
    return await create_test_user(UserRole.ADMIN)
