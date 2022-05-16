from typing import List

from xpresso import Depends, Operation, Path

from server.application.tags.queries import GetAllTags
from server.application.tags.views import TagView
from server.config.di import resolve
from server.seedwork.application.messages import MessageBus

from ..auth.dependencies import IsAuthenticated


async def list_tags() -> List[TagView]:
    bus = resolve(MessageBus)
    return await bus.execute(GetAllTags())


routes = [
    Path(
        "/",
        get=Operation(
            list_tags,
            dependencies=[Depends(IsAuthenticated())],
        ),
    )
]
