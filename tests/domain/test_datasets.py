from typing import List

import pytest

from server.application.datasets.queries import GetAllDatasets
from server.config.di import override, resolve
from server.domain.common.types import id_factory
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
        Dataset(id=id_factory(), title="mock0", description="mock0-desc"),
        Dataset(id=id_factory(), title="mock1", description="mock1-desc"),
        Dataset(id=id_factory(), title="mock2", description="mock2-desc"),
    ]

    with override() as container:
        container.register(
            DatasetRepository, instance=MockDatasetRepository(mock_datasets)
        )

        bus = resolve(MessageBus)

        query = GetAllDatasets()
        datasets = await bus.execute(query)

        assert datasets == mock_datasets
