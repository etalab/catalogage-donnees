from typing import List

from fastapi import APIRouter
from fastapi.exceptions import HTTPException

from server.application.datasets.commands import CreateDataset, DeleteDataset
from server.application.datasets.queries import GetAllDatasets, GetDatasetByID
from server.config.di import resolve
from server.domain.common.types import ID
from server.domain.datasets.entities import Dataset
from server.domain.datasets.exceptions import DatasetDoesNotExist
from server.seedwork.application.messages import MessageBus

from .schemas import DatasetCreate, DatasetRead

router = APIRouter(prefix="/datasets", tags=["datasets"])


@router.get("/", response_model=List[DatasetRead])
async def list_datasets() -> List[Dataset]:
    bus = resolve(MessageBus)

    query = GetAllDatasets()
    return await bus.execute(query)


@router.get("/{id}/", response_model=DatasetRead, responses={404: {}})
async def get_dataset_by_id(id: ID) -> Dataset:
    bus = resolve(MessageBus)

    query = GetDatasetByID(id=id)
    try:
        return await bus.execute(query)
    except DatasetDoesNotExist:
        raise HTTPException(404)


@router.post("/", response_model=DatasetRead, status_code=201)
async def create_dataset(data: DatasetCreate) -> Dataset:
    bus = resolve(MessageBus)

    command = CreateDataset(name=data.name)
    id = await bus.execute(command)

    query = GetDatasetByID(id=id)
    return await bus.execute(query)


@router.delete("/{id}/", status_code=204)
async def delete_dataset(id: ID) -> None:
    bus = resolve(MessageBus)

    command = DeleteDataset(id=id)
    await bus.execute(command)
