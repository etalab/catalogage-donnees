import datetime as dt

from pydantic import Field

from server.seedwork.domain.entities import Entity

from ..common import datetime as dtutil
from ..common.types import ID
from ..organizations.types import Siret


class CatalogRecord(Entity):
    id: ID
    organization_siret: Siret
    created_at: dt.datetime = Field(default_factory=dtutil.now)
