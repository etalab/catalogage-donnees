from pydantic import BaseModel

from server.domain.organizations.types import Siret


class OrganizationView(BaseModel):
    name: str
    siret: Siret
