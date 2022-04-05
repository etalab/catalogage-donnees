import datetime as dt
import enum
from typing import List, Optional

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


class UpdateFrequency(enum.Enum):
    NEVER = "never"
    REALTIME = "realtime"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"


class Dataset(Entity):
    id: ID
    created_at: dt.datetime = Field(default_factory=dtutil.now)
    title: str
    description: str
    formats: List[DataFormat]
    entrypoint_email: str
    contact_emails: List[str] = Field(default_factory=list)
    first_published_at: Optional[dt.datetime] = None
    update_frequency: Optional[UpdateFrequency] = None
    last_updated_at: Optional[dt.datetime] = None

    class Config:
        orm_mode = True

    def update(
        self,
        title: str,
        description: str,
        formats: List[DataFormat],
        entrypoint_email: str,
        contact_emails: List[str],
        first_published_at: Optional[dt.datetime],
        update_frequency: Optional[UpdateFrequency],
        last_updated_at: Optional[dt.datetime],
    ) -> None:
        self.title = title
        self.description = description
        self.formats = formats
        self.entrypoint_email = entrypoint_email
        self.contact_emails = contact_emails
        self.first_published_at = first_published_at
        self.update_frequency = update_frequency
        self.last_updated_at = last_updated_at
