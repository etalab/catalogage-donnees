from typing import List, Optional

from server.domain.common.pagination import Page, Pagination
from server.domain.common.types import ID
from server.domain.datasets.entities import GeographicalCoverage
from server.seedwork.application.queries import Query

from .views import DatasetSearchView, DatasetView


class GetAllDatasets(Query[Pagination[DatasetView]]):
    page: Page = Page()
    geographical_coverage: Optional[GeographicalCoverage] = None
    tag_ids: Optional[List[ID]] = None


class GetDatasetByID(Query[DatasetView]):
    id: ID


class SearchDatasets(Query[Pagination[DatasetSearchView]]):
    q: str
    page: Page = Page()
    highlight: bool = False
