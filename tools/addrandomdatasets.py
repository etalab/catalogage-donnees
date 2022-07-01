import argparse
import asyncio
import functools
import random

import aiometer
import click
from tqdm import tqdm

from server.application.tags.queries import GetAllTags
from server.config.di import bootstrap, resolve
from server.seedwork.application.messages import MessageBus
from tests.factories import CreateDatasetFactory

success = functools.partial(click.style, fg="bright_green")


async def main(n: int) -> None:
    bus = resolve(MessageBus)

    tag_id_set = [tag.id for tag in await bus.execute(GetAllTags())]

    with tqdm(total=n, unit="dataset") as progress:

        async def task() -> None:
            tag_ids = random.choices(tag_id_set, k=random.randint(1, 3))
            await bus.execute(CreateDatasetFactory.build(tag_ids=tag_ids))
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
