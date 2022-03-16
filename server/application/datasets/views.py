from typing import Optional

from server.domain.datasets.entities import Dataset
from server.domain.datasets.repositories import DatasetHeadlines


class DatasetSearchView(Dataset):
    headlines: Optional[DatasetHeadlines] = None
