from typing import List

from server.domain.common.types import ID
from server.seedwork.application.queries import Query

from .views import DatasetSearchView, DatasetView


class GetAllDatasets(Query[List[DatasetView]]):
    pass


class GetDatasetByID(Query[DatasetView]):
    id: ID


class SearchDatasets(Query[List[DatasetSearchView]]):
    q: str
    highlight: bool = False
