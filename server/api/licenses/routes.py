from typing import List

from fastapi import APIRouter, Depends

from server.application.licenses.queries import GetLicenseSet
from server.config.di import resolve
from server.seedwork.application.messages import MessageBus

from ..auth.dependencies import IsAuthenticated

router = APIRouter(prefix="/licenses", tags=["licenses"])


@router.get(
    "/",
    dependencies=[Depends(IsAuthenticated())],
    response_model=List[str],
)
async def list_licenses() -> List[str]:
    bus = resolve(MessageBus)
    return await bus.execute(GetLicenseSet())
