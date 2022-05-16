from typing import Union

from xpresso import (
    Depends,
    FromJson,
    FromPath,
    FromQuery,
    HTTPException,
    Operation,
    Path,
)
from xpresso.responses import ResponseSpec

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
from server.application.datasets.views import DatasetSearchView, DatasetView
from server.config.di import resolve
from server.domain.auth.entities import UserRole
from server.domain.common.pagination import Page, Pagination
from server.domain.common.types import ID
from server.domain.datasets.exceptions import DatasetDoesNotExist
from server.seedwork.application.messages import MessageBus

from ..auth.dependencies import HasRole, IsAuthenticated
from .schemas import DatasetCreate, DatasetListParams, DatasetUpdate


async def list_datasets(
    params: FromQuery[DatasetListParams],
) -> Union[Pagination[DatasetSearchView], Pagination[DatasetView]]:
    bus = resolve(MessageBus)

    page = Page(number=params.page_number, size=params.page_size)

    if params.q is not None:
        query = SearchDatasets(q=params.q, highlight=params.highlight, page=page)
        return await bus.execute(query)

    query = GetAllDatasets(page=page)
    return await bus.execute(query)


async def get_dataset_by_id(id: FromPath[ID]) -> DatasetView:
    bus = resolve(MessageBus)

    query = GetDatasetByID(id=id)
    try:
        return await bus.execute(query)
    except DatasetDoesNotExist:
        raise HTTPException(404)


async def create_dataset(data: FromJson[DatasetCreate]) -> DatasetView:
    bus = resolve(MessageBus)

    command = CreateDataset(**data.dict())

    id = await bus.execute(command)

    query = GetDatasetByID(id=id)
    return await bus.execute(query)


async def update_dataset(
    id: FromPath[ID], data: FromJson[DatasetUpdate]
) -> DatasetView:
    bus = resolve(MessageBus)

    command = UpdateDataset(id=id, **data.dict())

    try:
        await bus.execute(command)
    except DatasetDoesNotExist:
        raise HTTPException(404)

    query = GetDatasetByID(id=id)
    return await bus.execute(query)


async def delete_dataset(id: FromPath[ID]) -> None:
    bus = resolve(MessageBus)

    command = DeleteDataset(id=id)
    await bus.execute(command)


routes = [
    Path(
        "/",
        dependencies=[Depends(IsAuthenticated())],
        get=Operation(
            list_datasets,
        ),
        post=Operation(
            create_dataset,
            response_status_code=201,
        ),
    ),
    Path(
        "/{id}/",
        dependencies=[Depends(IsAuthenticated())],
        get=Operation(
            get_dataset_by_id,
            responses={404: ResponseSpec()},
        ),
        put=Operation(
            update_dataset,
            responses={404: ResponseSpec()},
        ),
        delete=Operation(
            delete_dataset,
            dependencies=[Depends(HasRole(UserRole.ADMIN))],
            response_status_code=204,
        ),
    ),
]
