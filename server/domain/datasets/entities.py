from server.seedwork.domain.entities import Entity

from ..common.types import ID


class Dataset(Entity):
    id: ID
    name: str

    class Config:
        orm_mode = True
