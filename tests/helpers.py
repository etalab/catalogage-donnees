from contextlib import asynccontextmanager
from typing import AsyncIterator

from server.application.auth.commands import CreateUser, DeleteUser
from server.application.auth.queries import GetUserByEmail
from server.config.di import resolve
from server.domain.auth.entities import User
from server.seedwork.application.messages import MessageBus


class _DisablePytestCollectionMixin:
    """
    Prevent a class named 'Test*' from being collected as a test case by pytest.

    See: https://github.com/pytest-dev/pytest/issues/1879
    """

    __test__ = False


class TestUser(_DisablePytestCollectionMixin, User):
    """
    A user that exposes the plaintext password for testing purposes.
    """

    password: str


@asynccontextmanager
async def temp_user() -> AsyncIterator[TestUser]:
    bus = resolve(MessageBus)

    email = "temp@example.org"
    password = "s3kr3t"

    command = CreateUser(email=email, password=password)
    await bus.execute(command)

    query = GetUserByEmail(email=email)
    user = await bus.execute(query)

    try:
        yield TestUser(**user.dict(), password=password)
    finally:
        command = DeleteUser(id=user.id)
        await bus.execute(command)
