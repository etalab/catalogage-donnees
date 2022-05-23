import itertools
from typing import Callable

import httpx

from server.application.auth.commands import CreateUser
from server.config.di import resolve
from server.domain.auth.entities import User, UserRole
from server.domain.auth.repositories import UserRepository
from server.seedwork.application.messages import MessageBus


def create_client(app: Callable) -> httpx.AsyncClient:
    return httpx.AsyncClient(app=app, base_url="http://testserver")


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

    def auth(self, request: httpx.Request) -> httpx.Request:
        """An auth function for use with HTTPX.

        Usage:
            response = client.post(..., auth=test_user.auth)
        """
        request.headers["Authorization"] = f"Bearer {self.api_token}"
        return request


_temp_user_ids = itertools.count(0)


async def create_test_user(role: UserRole) -> TestUser:
    bus = resolve(MessageBus)
    user_repository = resolve(UserRepository)

    email = f"temp{next(_temp_user_ids)}@mydomain.org"
    password = "s3kr3t"

    command = CreateUser(email=email, password=password)
    await bus.execute(command, role=role)

    user = await user_repository.get_by_email(email)
    assert user is not None

    return TestUser(**user.dict(), password=password)
