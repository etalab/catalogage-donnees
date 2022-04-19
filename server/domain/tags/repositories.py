from typing import List, Optional

from server.domain.common.types import ID, id_factory
from server.seedwork.domain.repositories import Repository

from .entities import Tag


class TagRepository(Repository):
    def make_id(self) -> ID:
        return id_factory()

    async def get_by_id(self, id_: ID) -> Optional[Tag]:
        raise NotImplementedError  # pragma: no cover

    async def get_all_by_ids(self, ids: List[ID]) -> List[Tag]:
        raise NotImplementedError  # pragma: no cover

    async def insert(self, entity: Tag) -> ID:
        raise NotImplementedError  # pragma: no cover
