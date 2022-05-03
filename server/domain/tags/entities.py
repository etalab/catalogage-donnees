from server.domain.common.types import ID
from server.seedwork.domain.entities import Entity


class Tag(Entity):
    id: ID
    name: str
