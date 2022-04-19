from typing import List

from server.config.di import resolve
from server.domain.common.types import ID
from server.domain.datasets.entities import Dataset
from server.domain.datasets.exceptions import DatasetDoesNotExist
from server.domain.datasets.repositories import DatasetRepository

from .commands import CreateDataset, DeleteDataset, UpdateDataset
from .queries import GetAllDatasets, GetDatasetByID, SearchDatasets
from .views import DatasetSearchView, DatasetView


async def create_dataset(command: CreateDataset, *, id_: ID = None) -> ID:
    repository = resolve(DatasetRepository)

    if id_ is None:
        id_ = repository.make_id()

    dataset = Dataset(id=id_, **command.dict())

    return await repository.insert(dataset)


async def update_dataset(command: UpdateDataset) -> None:
    repository = resolve(DatasetRepository)

    pk = command.id
    dataset = await repository.get_by_id(pk)
    if dataset is None:
        raise DatasetDoesNotExist(pk)

    dataset.update(**command.dict(exclude={"id"}))

    await repository.update(dataset)


async def delete_dataset(command: DeleteDataset) -> None:
    repository = resolve(DatasetRepository)
    await repository.delete(command.id)


async def get_all_datasets(query: GetAllDatasets) -> List[DatasetView]:
    repository = resolve(DatasetRepository)
    datasets = await repository.get_all()
    return [DatasetView(**dataset.dict()) for dataset in datasets]


async def get_dataset_by_id(query: GetDatasetByID) -> DatasetView:
    repository = resolve(DatasetRepository)

    id = query.id
    dataset = await repository.get_by_id(id)

    if dataset is None:
        raise DatasetDoesNotExist(id)

    return DatasetView(**dataset.dict())


async def search_datasets(query: SearchDatasets) -> List[DatasetSearchView]:
    repository = resolve(DatasetRepository)

    items = await repository.search(q=query.q, highlight=query.highlight)

    return [
        DatasetSearchView(
            **dataset.dict(),
            headlines=headlines,
        )
        for dataset, headlines in items
    ]
