import datetime as dt

from pydantic import BaseModel

from server.domain.common.types import ID
from server.domain.organizations.types import Siret


class CatalogRecordView(BaseModel):
    id: ID
    organization_siret: Siret
    created_at: dt.datetime
