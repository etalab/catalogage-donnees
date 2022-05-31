import datetime as dt
from typing import List, Optional

from fastapi import Query
from pydantic import BaseModel, EmailStr, Field

from server.domain.common.pagination import PAGE_NUMBER_CONSTR, PAGE_SIZE_CONSTR
from server.domain.common.types import ID
from server.domain.datasets.entities import (
    DataFormat,
    GeographicalCoverage,
    UpdateFrequency,
)


class DatasetListParams(BaseModel):
    q: str = Query(None)
    highlight: bool = Query(False)
    page_number: int = Query(1, **PAGE_NUMBER_CONSTR)
    page_size: int = Query(10, **PAGE_SIZE_CONSTR)


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
