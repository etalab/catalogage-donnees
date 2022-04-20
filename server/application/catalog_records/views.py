import datetime as dt

from pydantic import BaseModel


class CatalogRecordView(BaseModel):
    created_at: dt.datetime
