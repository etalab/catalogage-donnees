from typing import List

from server.domain.common.types import ID
from server.domain.datasets.entities import Dataset
from server.seedwork.application.queries import Query

from .views import DatasetSearchView


class GetAllDatasets(Query[List[Dataset]]):
    pass


class GetDatasetByID(Query[Dataset]):
    id: ID


class SearchDatasets(Query[List[DatasetSearchView]]):
    q: str
    highlight: bool = False
