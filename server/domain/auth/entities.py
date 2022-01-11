from server.seedwork.domain.entities import Entity

from ..common.types import ID


class User(Entity):
    id: ID
    email: str

    class Config:
        orm_mode = True
