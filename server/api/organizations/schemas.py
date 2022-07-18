from pydantic import BaseModel

from server.domain.organizations.types import Siret


class OrganizationCreate(BaseModel):
    name: str
    siret: Siret
