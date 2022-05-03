from pydantic import BaseModel

from server.domain.common.types import ID


class TagView(BaseModel):
    id: ID
    name: str
