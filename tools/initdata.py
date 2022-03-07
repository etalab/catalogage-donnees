import argparse
import asyncio
import pathlib

import yaml
from rich.console import Console

from server.application.auth.commands import CreateUser
from server.application.datasets.commands import CreateDataset, UpdateDataset
from server.config.di import bootstrap, resolve
from server.domain.auth.repositories import UserRepository
from server.domain.datasets.repositories import DatasetRepository
from server.seedwork.application.messages import MessageBus

spec_path = pathlib.Path(__file__).parent / "initdata.yml"

with spec_path.open() as f:
    spec = yaml.safe_load(f)


async def main(reset: bool = False) -> None:
    console = Console()

    bus = resolve(MessageBus)

    dataset_repository = resolve(DatasetRepository)
    user_repository = resolve(UserRepository)

    # --- Users ---

    console.rule("Users")

    for item in spec["users"]:
        email = item["params"]["email"]
        existing_user = await user_repository.get_by_email(email)

        if existing_user is not None:
            console.print(f"[blue]ok[/]: User(email={email!r})")
            continue

        command = CreateUser(**item["params"])
        await bus.execute(command, id_=item["id"])
        console.print(f"[bright_green]created[/]: {command!r}")

    # --- Datasets ---

    console.rule("Datasets")

    for item in spec["datasets"]:
        id_ = item["id"]
        existing_dataset = await dataset_repository.get_by_id(id_)

        if existing_dataset is not None:
            command = UpdateDataset(id=id_, **item["params"])

            changes = {
                k: getattr(command, k)
                for k in item["params"]
                if getattr(command, k) != getattr(existing_dataset, k)
            }

            if not changes or not reset:
                console.print(
                    f"[blue]ok[/]: "
                    f"Dataset(id={id_!r}, title={item['params']['title']!r})"
                )
                continue

            await bus.execute(command)
            console.print(f"[orange3]reset[/]: {command!r}")
            continue

        command = CreateDataset(**item["params"])
        await bus.execute(command, id_=id_)
        console.print(f"[bright_green]created[/]: {command!r}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--reset", action="store_true")
    args = parser.parse_args()

    bootstrap()

    asyncio.run(main(reset=args.reset))
