import argparse
import asyncio
import functools
import os
import pathlib
from typing import Dict

import click
import yaml
from dotenv import load_dotenv
from pydantic import BaseModel

from server.application.auth.commands import CreateUser
from server.application.datasets.commands import CreateDataset, UpdateDataset
from server.config.di import bootstrap, resolve
from server.domain.auth.entities import UserRole
from server.domain.auth.repositories import UserRepository
from server.domain.datasets.repositories import DatasetRepository
from server.seedwork.application.messages import MessageBus

load_dotenv()

info = functools.partial(click.style, fg="blue")
success = functools.partial(click.style, fg="bright_green")
warn = functools.partial(click.style, fg="yellow")
error = functools.partial(click.style, fg="red")


def ruler(text: str) -> str:
    return click.style(f"──── {text}", fg="magenta")


class UserExtras(BaseModel):
    role: UserRole = UserRole.USER


def _parse_env_passwords(passwords_env: str) -> Dict[str, str]:
    if not passwords_env:
        return {}
    passwords = {}
    for pair in passwords_env.split(","):
        email, password = pair.split("=")
        passwords[email] = password
    return passwords


async def handle_user(
    item: dict, *, no_input: bool, env_passwords: Dict[str, str]
) -> None:
    bus = resolve(MessageBus)
    repository = resolve(UserRepository)

    email = item["params"]["email"]
    existing_user = await repository.get_by_email(email)

    if existing_user is not None:
        print(f"{info('ok')}: User(email={email!r}, ...)")
        return

    extras = UserExtras(**item.get("extras", {}))

    if item["params"]["password"] == "__env__":
        password = env_passwords.get(email)
        if password is None:
            if no_input:
                raise RuntimeError(
                    f"would prompt password for {email!r}, "
                    "please include '<email>=<password>' in TOOLS_PASSWORDS "
                    "environment variable"
                )
            password = click.prompt(f"Password for {email}", hide_input=True)
        item["params"]["password"] = password

    command = CreateUser(**item["params"])
    await bus.execute(command, id_=item["id"], **extras.dict())
    print(f"{success('created')}: {command!r}")


async def handle_dataset(item: dict, reset: bool = False) -> None:
    bus = resolve(MessageBus)
    repository = resolve(DatasetRepository)

    id_ = item["id"]
    existing_dataset = await repository.get_by_id(id_)

    if existing_dataset is not None:
        command = UpdateDataset(id=id_, **item["params"])

        changed = any(
            getattr(command, k) != getattr(existing_dataset, k) for k in item["params"]
        )

        if changed and reset:
            await bus.execute(command)
            print(f"{warn('reset')}: {command!r}")
            return

        dataset_repr = f"Dataset(id={id_!r}, title={item['params']['title']!r}, ...)"
        print(f"{info('ok')}: {dataset_repr}")
        return

    command = CreateDataset(**item["params"])

    await bus.execute(command, id_=id_)
    print(f"{success('created')}: {command!r}")


async def main(path: pathlib.Path, reset: bool = False, no_input: bool = False) -> None:
    with path.open() as f:
        spec = yaml.safe_load(f)

    print("\n", ruler("Users"))

    env_passwords = _parse_env_passwords(os.getenv("TOOLS_PASSWORDS", ""))

    for item in spec["users"]:
        await handle_user(item, no_input=no_input, env_passwords=env_passwords)

    print("\n", ruler("Datasets"))

    for item in spec["datasets"]:
        await handle_dataset(item, reset=reset)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=pathlib.Path)
    parser.add_argument("--reset", action="store_true")
    args = parser.parse_args()

    bootstrap()

    asyncio.run(main(path=args.path, reset=args.reset))
