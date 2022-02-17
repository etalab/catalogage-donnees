import enum
from typing import List

from server.seedwork.domain.entities import Entity

from ..common.types import ID


class DataFormat(enum.Enum):
    FILE_TABULAR = "file_tabular"
    FILE_GIS = "file_gis"
    API = "api"
    DATABASE = "database"
    WEBSITE = "website"
    OTHER = "other"


class Dataset(Entity):
    id: ID
    title: str
    description: str
    formats: List[DataFormat]

    class Config:
        orm_mode = True

    def update(self, title: str, description: str, formats: List[DataFormat]) -> None:
        self.title = title
        self.description = description
        self.formats = formats
