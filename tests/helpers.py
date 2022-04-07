import datetime as dt
import itertools

import httpx
from _pytest.python_api import ApproxBase

from server.application.auth.commands import CreateUser
from server.application.auth.queries import GetUserByEmail
from server.config.di import resolve
from server.domain.auth.entities import User, UserRole
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

    email = f"temp{next(_temp_user_ids)}@example.org"
    password = "s3kr3t"

    command = CreateUser(email=email, password=password)
    await bus.execute(command, role=role)

    query = GetUserByEmail(email=email)
    user = await bus.execute(query)

    return TestUser(**user.dict(), password=password)


class approx_datetime(ApproxBase):
    """
    An equivalent of pytest.approx() for approximating datetimes.

    See: https://github.com/pytest-dev/pytest/issues/8395#issuecomment-790549327
    """

    def __init__(self, expected: dt.datetime, abs: dt.timedelta) -> None:
        if abs < dt.timedelta(0):
            raise ValueError(f"absolute tolerance cannot be negative: {abs}")
        super().__init__(expected, abs=abs)

    def __repr__(self) -> str:
        return f"approx_datetime({self.expected!r} ± {self.abs!r}"

    def __eq__(self, actual: object) -> bool:
        return abs(self.expected - actual) <= self.abs
