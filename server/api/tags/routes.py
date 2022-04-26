from typing import List

from fastapi import APIRouter, Depends

from server.application.tags.queries import GetAllTags
from server.application.tags.views import TagView
from server.config.di import resolve
from server.seedwork.application.messages import MessageBus

from ..auth.dependencies import IsAuthenticated

router = APIRouter(prefix="/tags", tags=["tags"])


@router.get(
    "/",
    dependencies=[Depends(IsAuthenticated())],
    response_model=List[TagView],
)
async def list_tags() -> List[TagView]:
    bus = resolve(MessageBus)
    return await bus.execute(GetAllTags())
