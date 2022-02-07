from pydantic import BaseModel, validator

from server.domain.common.types import ID


class DatasetRead(BaseModel):
    id: ID
    title: str
    description: str


class DatasetCreate(BaseModel):
    title: str
    description: str


class DatasetUpdate(BaseModel):
    title: str
    description: str

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
