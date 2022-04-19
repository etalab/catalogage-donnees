import argparse
import asyncio
import functools
from pathlib import Path
from typing import List

import click
import yaml

from server.domain.common.types import id_factory

info = functools.partial(click.style, fg="blue")
success = functools.partial(click.style, fg="bright_green")


def _check_unique(names: List[str]) -> None:
    assert len(names) == len(set(names)), "tags are not unique"


async def main(path: Path, output: Path) -> None:
    names = path.read_text().splitlines()
    _check_unique(names)

    if output.exists():
        with output.open("r") as f:
            spec = yaml.safe_load(f)
            _check_unique([tag["params"]["name"] for tag in spec["tags"]])
            existing_tag_ids_by_name = {
                tag["params"]["name"]: tag["id"] for tag in spec["tags"]
            }

    tags = []

    for name in names:
        try:
            id_ = existing_tag_ids_by_name[name]
            print(f"{info('exists')}: {name}")
        except KeyError:
            print(f"{success('new')}: {name}")
            id_ = str(id_factory())

        tags.append(
            {
                "id": id_,
                "params": {
                    "name": name,
                },
            }
        )

    spec = {
        "users": [],
        "datasets": [],
        "tags": tags,
    }

    with output.open("w") as f:
        yaml.safe_dump(spec, f)

    print(f"done: {output}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    asyncio.run(main(path=args.path, output=args.output))
