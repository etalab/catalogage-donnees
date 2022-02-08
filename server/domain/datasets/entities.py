from server.seedwork.domain.entities import Entity

from ..common.types import ID


class Dataset(Entity):
    id: ID
    title: str
    description: str

    class Config:
        orm_mode = True

    def update(self, title: str, description: str) -> None:
        self.title = title
        self.description = description
