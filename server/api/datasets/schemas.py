from pydantic import BaseModel

from server.domain.common.types import ID


class DatasetRead(BaseModel):
    id: ID
    name: str


class DatasetCreate(BaseModel):
    name: str
