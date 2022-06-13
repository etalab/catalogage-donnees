from typing import List, Optional, Tuple

from typing_extensions import TypedDict

from server.seedwork.domain.repositories import Repository

from ..common.pagination import Page
from ..common.types import ID, id_factory
from .entities import Dataset
from .specifications import DatasetSpec


class DatasetHeadlines(TypedDict):
    title: str
    description: Optional[str]


SearchResult = Tuple[Dataset, Optional[DatasetHeadlines]]


class DatasetRepository(Repository):
    def make_id(self) -> ID:
        return id_factory()

    async def get_all(
        self, *, page: Page = Page(), spec: DatasetSpec = DatasetSpec()
    ) -> Tuple[List[Dataset], int]:
        raise NotImplementedError  # pragma: no cover

    async def search(
        self, q: str, highlight: bool = False, page: Page = Page()
    ) -> Tuple[List[SearchResult], int]:
        raise NotImplementedError  # pragma: no cover

    async def get_by_id(self, id: ID) -> Optional[Dataset]:
        raise NotImplementedError  # pragma: no cover

    async def insert(self, entity: Dataset) -> ID:
        raise NotImplementedError  # pragma: no cover

    async def update(self, entity: Dataset) -> None:
        raise NotImplementedError  # pragma: no cover

    async def delete(self, id: ID) -> None:
        raise NotImplementedError  # pragma: no cover
