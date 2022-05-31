import pytest
from pydantic import EmailStr, SecretStr

from server.application.auth.commands import ChangePassword, CreateUser
from server.application.auth.queries import Login
from server.config.di import resolve
from server.domain.auth.exceptions import LoginFailed
from server.seedwork.application.messages import MessageBus


@pytest.mark.asyncio
async def test_changepassword() -> None:
    bus = resolve(MessageBus)
    email = EmailStr("changepassworduser@mydomain.org")

    await bus.execute(CreateUser(email=email, password=SecretStr("initialpwd")))

    await bus.execute(ChangePassword(email=email, password=SecretStr("newpwd")))

    with pytest.raises(LoginFailed):
        await bus.execute(Login(email=email, password=SecretStr("initialpwd")))

    await bus.execute(Login(email=email, password=SecretStr("newpwd")))
