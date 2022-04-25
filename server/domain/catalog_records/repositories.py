from typing import Optional

from server.seedwork.domain.repositories import Repository

from ..common.types import ID, id_factory
from .entities import CatalogRecord


class CatalogRecordRepository(Repository):
    def make_id(self) -> ID:
        return id_factory()

    async def get_by_id(self, id: ID) -> Optional[CatalogRecord]:
        raise NotImplementedError  # pragma: no cover

    async def insert(self, entity: CatalogRecord) -> ID:
        raise NotImplementedError  # pragma: no cover
