from pathlib import Path

import pytest
import yaml

from server.application.datasets.commands import UpdateDataset
from server.application.datasets.queries import GetAllDatasets, GetDatasetByID
from server.config.di import resolve
from server.seedwork.application.messages import MessageBus
from tools import initdata


@pytest.mark.asyncio
async def test_initdata_empty(tmp_path: Path) -> None:
    bus = resolve(MessageBus)

    spec: dict = {"users": [], "datasets": []}
    path = tmp_path / "initdata.yml"
    path.write_text(yaml.dump(spec))

    await initdata.main(path)

    assert await bus.execute(GetAllDatasets()) == []


@pytest.mark.asyncio
async def test_initdata(capsys: pytest.CaptureFixture) -> None:
    bus = resolve(MessageBus)
    path = Path("tools", "initdata.yml")

    # Initial run creates data items.
    await initdata.main(path)
    captured = capsys.readouterr()
    assert captured.out.count("created") == 4

    pk = "16b398af-f8c7-48b9-898a-18ad3404f528"
    dataset = await bus.execute(GetDatasetByID(id=pk))
    assert dataset.title == "Données brutes de l'inventaire forestier"

    # Run a second time, without changes.
    await initdata.main(path)
    captured = capsys.readouterr()
    assert captured.out.count("ok") == 4

    # Make a change.
    command = UpdateDataset(**dataset.dict(exclude={"title"}), title="Changed")
    await bus.execute(command)
    dataset = await bus.execute(GetDatasetByID(id=pk))
    assert dataset.title == "Changed"

    # No reset: dataset left unchanged
    await initdata.main(path)
    captured = capsys.readouterr()
    assert captured.out.count("ok") == 4
    dataset = await bus.execute(GetDatasetByID(id=pk))
    assert dataset.title == "Changed"

    # Reset: dataset goes back to initial state defined in yml file
    await initdata.main(path, reset=True)
    captured = capsys.readouterr()
    assert captured.out.count("ok") == 3, captured.out
    assert captured.out.count("reset") == 1
    dataset = await bus.execute(GetDatasetByID(id=pk))
    assert dataset.title == "Données brutes de l'inventaire forestier"

    # Reset: dataset left in initial state
    await initdata.main(path, reset=True)
    captured = capsys.readouterr()
    assert captured.out.count("ok") == 4
    dataset = await bus.execute(GetDatasetByID(id=pk))
    assert dataset.title == "Données brutes de l'inventaire forestier"
