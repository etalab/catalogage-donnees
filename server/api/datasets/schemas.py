import datetime as dt
from typing import List

from pydantic import BaseModel, EmailStr, Field, validator

from server.domain.common.types import ID
from server.domain.datasets.entities import DataFormat


class DatasetRead(BaseModel):
    id: ID
    created_at: dt.datetime
    title: str
    description: str
    formats: List[DataFormat]
    entrypoint_email: str
    contact_emails: List[str]


class DatasetCreate(BaseModel):
    title: str
    description: str
    formats: List[DataFormat]
    entrypoint_email: EmailStr
    contact_emails: List[EmailStr] = Field(default_factory=list)

    @validator("formats")
    def check_formats_at_least_one(cls, value: List[DataFormat]) -> List[DataFormat]:
        if not value:
            raise ValueError("formats must contain at least one item")
        return value


class DatasetUpdate(BaseModel):
    title: str
    description: str
    formats: List[DataFormat]
    entrypoint_email: EmailStr
    contact_emails: List[EmailStr]

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

    @validator("formats")
    def check_formats_at_least_one(cls, value: List[DataFormat]) -> List[DataFormat]:
        if not value:
            raise ValueError("formats must contain at least one item")
        return value
