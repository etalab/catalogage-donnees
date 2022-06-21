import json
from typing import Callable

import httpx
from pydantic import BaseModel

from server.config.di import resolve
from server.domain.auth.entities import User, UserRole
from server.domain.auth.repositories import UserRepository
from server.seedwork.application.messages import MessageBus

from .factories import CreateUserFactory


def create_client(app: Callable) -> httpx.AsyncClient:
    return httpx.AsyncClient(app=app, base_url="http://testserver")


def to_payload(obj: BaseModel) -> dict:
    """
    Convert a Pydantic model instance to a JSON-serializable dictionary.
    """
    return json.loads(obj.json())


class TestUser(User):
    """
    A user that exposes the plaintext password for testing purposes.
    """

    __test__ = False  # pytest shouldn't collect this.

    password: str

    def auth(self, request: httpx.Request) -> httpx.Request:
        """An auth function for use with HTTPX.

        Usage:
            response = client.post(..., auth=test_user.auth)
        """
        request.headers["Authorization"] = f"Bearer {self.api_token}"
        return request


async def create_test_user(role: UserRole) -> TestUser:
    bus = resolve(MessageBus)
    user_repository = resolve(UserRepository)

    command = CreateUserFactory.build()
    await bus.execute(command, role=role)

    user = await user_repository.get_by_email(command.email)
    assert user is not None

    return TestUser(**user.dict(), password=command.password.get_secret_value())
