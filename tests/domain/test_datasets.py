from typing import List

import pytest

from server.application.datasets.queries import GetAllDatasets
from server.config.di import override, resolve
from server.domain.datasets.entities import Dataset
from server.domain.datasets.repositories import DatasetRepository
from server.seedwork.application.messages import MessageBus


@pytest.mark.asyncio
async def test_datasets_get_all() -> None:
    class MockDatasetRepository(DatasetRepository):
        def __init__(self, items: List[Dataset]) -> None:
            self.items = items

        async def get_all(self) -> List[Dataset]:
            return self.items

    mock_datasets = [
        Dataset(id=0, name="mock0"),
        Dataset(id=1, name="mock1"),
        Dataset(id=2, name="mock2"),
    ]

    with override() as container:
        container.register(
            DatasetRepository, instance=MockDatasetRepository(mock_datasets)
        )

        bus = resolve(MessageBus)

        query = GetAllDatasets()
        datasets = await bus.execute(query)

        assert datasets == mock_datasets
