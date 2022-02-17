from typing import List

from pydantic import BaseModel, validator

from server.domain.common.types import ID
from server.domain.datasets.entities import DataFormat


class DatasetRead(BaseModel):
    id: ID
    title: str
    description: str
    formats: List[DataFormat]


class DatasetCreate(BaseModel):
    title: str
    description: str
    formats: List[DataFormat]

    @validator("formats")
    def check_formats_at_least_one(cls, value: List[DataFormat]) -> List[DataFormat]:
        if not value:
            raise ValueError("formats must contain at least one item")
        return value


class DatasetUpdate(BaseModel):
    title: str
    description: str
    formats: List[DataFormat]

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
