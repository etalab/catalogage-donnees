import datetime as dt
import enum
from typing import List

from pydantic import Field

from server.seedwork.domain.entities import Entity

from ..common import datetime as dtutil
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
    created_at: dt.datetime = Field(default_factory=dtutil.now)
    title: str
    description: str
    formats: List[DataFormat]

    class Config:
        orm_mode = True

    def update(self, title: str, description: str, formats: List[DataFormat]) -> None:
        self.title = title
        self.description = description
        self.formats = formats
