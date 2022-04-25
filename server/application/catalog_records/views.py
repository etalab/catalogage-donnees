import datetime as dt

from pydantic import BaseModel

from server.domain.common.types import ID


class CatalogRecordView(BaseModel):
    id: ID
    created_at: dt.datetime
