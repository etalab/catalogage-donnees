from pydantic import BaseModel

from server.domain.auth.entities import UserRole
from server.domain.common.types import ID
from server.domain.organizations.types import Siret


class UserView(BaseModel):
    id: ID
    organization_siret: Siret
    email: str
    role: UserRole


class AuthenticatedUserView(BaseModel):
    id: ID
    organization_siret: Siret
    email: str
    role: UserRole
    api_token: str
