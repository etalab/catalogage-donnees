import datetime as dt
from typing import List, Optional

from pydantic import BaseModel

from server.domain.common.types import ID
from server.domain.datasets.entities import (
    DataFormat,
    GeographicalCoverage,
    UpdateFrequency,
)
from server.domain.datasets.repositories import DatasetHeadlines


class DatasetView(BaseModel):
    id: ID
    created_at: dt.datetime
    title: str
    description: str
    service: str
    geographical_coverage: GeographicalCoverage
    formats: List[DataFormat]
    technical_source: Optional[str]
    entrypoint_email: str
    contact_emails: List[str]
    update_frequency: Optional[UpdateFrequency]
    last_updated_at: Optional[dt.datetime]


class DatasetSearchView(DatasetView):
    headlines: Optional[DatasetHeadlines] = None
