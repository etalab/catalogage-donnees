import argparse
import asyncio
import functools
import pathlib

import click
import yaml

from server.application.auth.commands import CreateUser
from server.application.datasets.commands import CreateDataset, UpdateDataset
from server.config.di import bootstrap, resolve
from server.domain.auth.repositories import UserRepository
from server.domain.datasets.repositories import DatasetRepository
from server.seedwork.application.messages import MessageBus

info = functools.partial(click.style, fg="blue")
success = functools.partial(click.style, fg="bright_green")
warn = functools.partial(click.style, fg="yellow")


def ruler(text: str) -> str:
    return click.style(f"──── {text}", fg="magenta")


async def handle_user(item: dict) -> None:
    bus = resolve(MessageBus)
    repository = resolve(UserRepository)

    email = item["params"]["email"]
    existing_user = await repository.get_by_email(email)

    if existing_user is not None:
        print(f"{info('ok')}: User(email={email!r}, ...)")
        return

    command = CreateUser(**item["params"])
    await bus.execute(command, id_=item["id"])
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

        result = "unchanged" if reset else "ok"
        dataset_repr = f"Dataset(id={id_!r}, title={item['params']['title']!r}, ...)"
        print(f"{info(result)}: {dataset_repr}")
        return

    command = CreateDataset(**item["params"])

    await bus.execute(command, id_=id_)
    print(f"{success('created')}: {command!r}")


async def main(path: pathlib.Path, reset: bool = False) -> None:
    with path.open() as f:
        spec = yaml.safe_load(f)

    print("\n", ruler("Users"))

    for item in spec["users"]:
        await handle_user(item)

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
