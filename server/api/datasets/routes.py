from typing import List, Union

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse

from server.application.datasets.commands import (
    CreateDataset,
    DeleteDataset,
    UpdateDataset,
)
from server.application.datasets.queries import (
    GetAllDatasets,
    GetDatasetByID,
    SearchDatasets,
)
from server.config.di import resolve
from server.domain.auth.entities import UserRole
from server.domain.common.types import ID
from server.domain.datasets.entities import Dataset
from server.domain.datasets.exceptions import DatasetDoesNotExist
from server.seedwork.application.messages import MessageBus

from ..auth.dependencies import HasRole, IsAuthenticated
from .schemas import DatasetCreate, DatasetRead, DatasetUpdate

router = APIRouter(prefix="/datasets", tags=["datasets"])


@router.get("/", response_model=List[DatasetRead])
async def list_datasets(
    q: str = None, highlight: bool = False
) -> Union[JSONResponse, List[Dataset]]:
    bus = resolve(MessageBus)

    if q is not None:
        query = SearchDatasets(q=q, highlight=highlight)
        items = await bus.execute(query)
        return JSONResponse(jsonable_encoder(items))

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

    command = CreateDataset(**data.dict())

    id = await bus.execute(command)

    query = GetDatasetByID(id=id)
    return await bus.execute(query)


@router.put("/{id}/", response_model=DatasetRead, responses={404: {}})
async def update_dataset(id: ID, data: DatasetUpdate) -> Dataset:
    bus = resolve(MessageBus)

    command = UpdateDataset(id=id, **data.dict())

    try:
        await bus.execute(command)
    except DatasetDoesNotExist:
        raise HTTPException(404)

    query = GetDatasetByID(id=id)
    return await bus.execute(query)


@router.delete(
    "/{id}/",
    dependencies=[Depends(IsAuthenticated()), Depends(HasRole(UserRole.ADMIN))],
    status_code=204,
)
async def delete_dataset(id: ID) -> None:
    bus = resolve(MessageBus)

    command = DeleteDataset(id=id)
    await bus.execute(command)
