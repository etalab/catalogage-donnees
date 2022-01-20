from typing import List

from server.config.di import resolve
from server.domain.common.types import ID
from server.domain.datasets.entities import Dataset
from server.domain.datasets.exceptions import DatasetDoesNotExist
from server.domain.datasets.repositories import DatasetRepository

from .commands import CreateDataset, DeleteDataset
from .queries import GetAllDatasets, GetDatasetByID


async def create_dataset(command: CreateDataset) -> ID:
    repository = resolve(DatasetRepository)
    dataset = Dataset(id=repository.make_id(), name=command.name)
    return await repository.insert(dataset)


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
