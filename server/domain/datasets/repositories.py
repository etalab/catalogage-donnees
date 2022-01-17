from typing import List, Optional

from server.seedwork.domain.repositories import Repository

from ..common.types import ID
from .entities import Dataset


class DatasetRepository(Repository):
    async def get_all(self) -> List[Dataset]:
        raise NotImplementedError

    async def get_by_id(self, id: ID) -> Optional[Dataset]:
        raise NotImplementedError

    async def insert(self, entity: Dataset) -> ID:
        raise NotImplementedError

    async def delete(self, id: ID) -> None:
        raise NotImplementedError
