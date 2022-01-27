from pydantic import BaseModel

from server.domain.common.types import ID


class DatasetRead(BaseModel):
    id: ID
    title: str
    description: str


class DatasetCreate(BaseModel):
    title: str
    description: str
