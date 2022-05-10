from server.domain.common.pagination import Page, Pagination
from server.domain.common.types import ID
from server.seedwork.application.queries import Query

from .views import DatasetSearchView, DatasetView


class GetAllDatasets(Query[Pagination[DatasetView]]):
    page: Page = Page()


class GetDatasetByID(Query[DatasetView]):
    id: ID


class SearchDatasets(Query[Pagination[DatasetSearchView]]):
    q: str
    page: Page = Page()
    highlight: bool = False
