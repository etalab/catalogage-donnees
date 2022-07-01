import argparse
import asyncio
import functools

import aiometer
import click
from tqdm import tqdm

from server.config.di import bootstrap, resolve
from server.seedwork.application.messages import MessageBus
from tests.factories import CreateDatasetFactory

success = functools.partial(click.style, fg="bright_green")


async def main(n: int) -> None:
    bus = resolve(MessageBus)

    with tqdm(total=n, unit="dataset") as progress:

        async def task() -> None:
            await bus.execute(CreateDatasetFactory.build())
            progress.update()

        tasks = [task for _ in range(n)]
        await aiometer.run_all(tasks, max_at_once=20)

    print(f"{success('created')}: {n} datasets")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("n", type=int)
    args = parser.parse_args()

    bootstrap()
    asyncio.run(main(n=args.n))
