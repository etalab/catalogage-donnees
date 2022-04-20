import datetime as dt

from pydantic import Field

from server.seedwork.domain.entities import Entity

from ..common import datetime as dtutil
from ..common.types import ID


class CatalogRecord(Entity):
    id: ID
    created_at: dt.datetime = Field(default_factory=dtutil.now)
