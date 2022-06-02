import datetime as dt
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field

from server.domain.common.types import ID
from server.domain.datasets.entities import (
    DataFormat,
    GeographicalCoverage,
    UpdateFrequency,
)

# See: https://github.com/tiangolo/fastapi/issues/318#issuecomment-584087181


class DatasetCreate(BaseModel):
    title: str
    description: str
    service: str
    geographical_coverage: GeographicalCoverage
    formats: List[DataFormat]
    technical_source: Optional[str] = None
    producer_email: Optional[EmailStr] = None
    contact_emails: List[EmailStr]
    update_frequency: Optional[UpdateFrequency] = None
    last_updated_at: Optional[dt.datetime] = None
    published_url: Optional[str] = None
    tag_ids: List[ID] = Field(default_factory=list)


class DatasetUpdate(BaseModel):
    title: str
    description: str
    service: str
    geographical_coverage: GeographicalCoverage
    formats: List[DataFormat]
    technical_source: Optional[str] = Field(...)
    producer_email: Optional[EmailStr] = Field(...)
    contact_emails: List[EmailStr]
    update_frequency: Optional[UpdateFrequency] = Field(...)
    last_updated_at: Optional[dt.datetime] = Field(...)
    published_url: Optional[str] = Field(...)
    tag_ids: List[ID]
