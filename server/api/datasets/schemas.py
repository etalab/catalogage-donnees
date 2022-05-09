import datetime as dt
from typing import List, Optional

from fastapi import Query
from pydantic import BaseModel, EmailStr, Field, validator

from server.domain.common.types import ID
from server.domain.datasets.entities import (
    DataFormat,
    GeographicalCoverage,
    UpdateFrequency,
)


class DatasetListParams(BaseModel):
    q: str = Query(None)
    highlight: bool = Query(False)


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

    @validator("formats")
    def check_formats_at_least_one(cls, value: List[DataFormat]) -> List[DataFormat]:
        if not value:
            raise ValueError("formats must contain at least one item")
        return value

    @validator("contact_emails")
    def check_contact_emails_at_least_one(cls, value: List[str]) -> List[str]:
        if not value:
            raise ValueError("contact_emails must contain at least one item")
        return value


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

    @validator("title")
    def check_title_not_empty(cls, value: str) -> str:
        if not value:
            raise ValueError("title must not be empty")
        return value

    @validator("description")
    def check_description_not_empty(cls, value: str) -> str:
        if not value:
            raise ValueError("description must not be empty")
        return value

    @validator("service")
    def check_service_not_empty(cls, value: str) -> str:
        if not value:
            raise ValueError("service must not be empty")
        return value

    @validator("formats")
    def check_formats_at_least_one(cls, value: List[DataFormat]) -> List[DataFormat]:
        if not value:
            raise ValueError("formats must contain at least one item")
        return value

    @validator("contact_emails")
    def check_contact_emails_at_least_one(cls, value: List[str]) -> List[str]:
        if not value:
            raise ValueError("contact_emails must contain at least one item")
        return value

    @validator("published_url")
    def check_published_url_not_empty(cls, value: Optional[str]) -> Optional[str]:
        if value is not None and not value:
            raise ValueError("published_url must not be empty")
        return value
