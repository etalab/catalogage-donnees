from typing import List

from server.domain.common.types import ID
from server.domain.datasets.entities import Dataset
from server.seedwork.application.queries import Query


class GetAllDatasets(Query[List[Dataset]]):
    pass


class GetDatasetByID(Query[Dataset]):
    id: ID


class SearchDatasets(Query[List[Dataset]]):
    q: str
