import datetime as dt
import enum
from typing import List, Optional

from pydantic import Field

from server.domain.tags.entities import Tag
from server.seedwork.domain.entities import Entity

from ..catalog_records.entities import CatalogRecord
from ..common.types import ID


class GeographicalCoverage(enum.Enum):
    MUNICIPALITY = "municipality"
    EPCI = "epci"
    DEPARTMENT = "department"
    REGION = "region"
    NATIONAL = "national"
    NATIONAL_FULL_TERRITORY = "national_full_territory"
    EUROPE = "europe"
    WORLD = "world"


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
    catalog_record: CatalogRecord
    title: str
    description: str
    service: str
    geographical_coverage: GeographicalCoverage
    formats: List[DataFormat]
    technical_source: Optional[str]
    producer_email: Optional[str]
    contact_emails: List[str]
    update_frequency: Optional[UpdateFrequency] = None
    last_updated_at: Optional[dt.datetime] = None
    url: Optional[str] = None
    tags: List[Tag] = Field(default_factory=list)

    class Config:
        orm_mode = True

    def update(
        self,
        title: str,
        description: str,
        service: str,
        geographical_coverage: GeographicalCoverage,
        formats: List[DataFormat],
        technical_source: Optional[str],
        producer_email: Optional[str],
        contact_emails: List[str],
        update_frequency: Optional[UpdateFrequency],
        last_updated_at: Optional[dt.datetime],
        url: Optional[str],
        tags: List[Tag],
    ) -> None:
        self.title = title
        self.description = description
        self.service = service
        self.geographical_coverage = geographical_coverage
        self.formats = formats
        self.technical_source = technical_source
        self.producer_email = producer_email
        self.contact_emails = contact_emails
        self.update_frequency = update_frequency
        self.last_updated_at = last_updated_at
        self.url = url
        self.tags = tags
