from typing import List

from server.config.di import resolve
from server.domain.common.types import ID
from server.domain.datasets.entities import Dataset
from server.domain.datasets.exceptions import DatasetDoesNotExist
from server.domain.datasets.repositories import DatasetRepository

from .commands import CreateDataset, DeleteDataset, UpdateDataset
from .queries import GetAllDatasets, GetDatasetByID, SearchDatasets


async def create_dataset(command: CreateDataset, *, id_: ID = None) -> ID:
    repository = resolve(DatasetRepository)

    if id_ is None:
        id_ = repository.make_id()

    dataset = Dataset(
        id=id_,
        title=command.title,
        description=command.description,
        formats=command.formats,
    )

    return await repository.insert(dataset)


async def update_dataset(command: UpdateDataset) -> None:
    repository = resolve(DatasetRepository)

    pk = command.id
    dataset = await repository.get_by_id(pk)
    if dataset is None:
        raise DatasetDoesNotExist(pk)

    dataset.update(
        title=command.title,
        description=command.description,
        formats=command.formats,
    )

    await repository.update(dataset)


async def delete_dataset(command: DeleteDataset) -> None:
    repository = resolve(DatasetRepository)
    await repository.delete(command.id)


async def get_all_datasets(query: GetAllDatasets) -> List[Dataset]:
    repository = resolve(DatasetRepository)
    return await repository.get_all()


async def get_dataset_by_id(query: GetDatasetByID) -> Dataset:
    repository = resolve(DatasetRepository)

    id = query.id
    dataset = await repository.get_by_id(id)

    if dataset is None:
        raise DatasetDoesNotExist(id)

    return dataset


async def search_datasets(query: SearchDatasets) -> List[Dataset]:
    repository = resolve(DatasetRepository)
    return await repository.search(q=query.q)
