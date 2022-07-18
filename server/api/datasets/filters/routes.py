from fastapi import APIRouter, Depends

from server.api.auth.permissions import IsAuthenticated
from server.application.datasets.queries import GetDatasetFilters
from server.application.datasets.views import DatasetFiltersView
from server.config.di import resolve
from server.seedwork.application.messages import MessageBus

router = APIRouter(prefix="/filters")


@router.get(
    "/",
    dependencies=[Depends(IsAuthenticated())],
    response_model=DatasetFiltersView,
)
async def get_dataset_filters() -> DatasetFiltersView:
    bus = resolve(MessageBus)
    return await bus.execute(GetDatasetFilters())
