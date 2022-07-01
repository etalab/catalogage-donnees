import pytest

from server.application.datasets.queries import GetAllDatasets
from server.config.di import resolve
from server.infrastructure.database import Database
from server.seedwork.application.messages import MessageBus
from tools import addrandomdatasets


@pytest.mark.asyncio
async def test_addrandomdatasets() -> None:
    bus = resolve(MessageBus)
    db = resolve(Database)

    async with db.autorollback():
        pagination = await bus.execute(GetAllDatasets())
        assert pagination.total_items == 0

        await addrandomdatasets.main(n=100)

        pagination = await bus.execute(GetAllDatasets())
        assert pagination.total_items == 100
