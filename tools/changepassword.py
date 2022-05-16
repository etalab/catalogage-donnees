import asyncio
import sys

import click
from pydantic import SecretStr

from server.application.auth.commands import ChangePassword
from server.config.di import bootstrap, resolve
from server.domain.auth.entities import User
from server.domain.auth.repositories import UserRepository
from server.seedwork.application.messages import MessageBus


async def _prompt_user() -> User:
    repository = resolve(UserRepository)

    email = click.prompt("Email")

    user = await repository.get_by_email(email)

    if user is None:
        click.echo(click.style(f"User does not exist: {email}", fg="red"))
        sys.exit(1)

    return user


def _prompt_password() -> SecretStr:
    return click.prompt(
        "Password",
        confirmation_prompt="Password (repeat)",
        value_proc=SecretStr,
        hide_input=True,
    )


async def main() -> None:
    bus = resolve(MessageBus)

    user = await _prompt_user()
    password = _prompt_password()

    await bus.execute(ChangePassword(email=user.email, password=password))


if __name__ == "__main__":
    bootstrap()
    asyncio.run(main())
