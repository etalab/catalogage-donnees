import enum

from server.seedwork.domain.entities import Entity

from ..common.types import ID
from ..organizations.types import Siret


class UserRole(enum.Enum):
    USER = "USER"
    ADMIN = "ADMIN"


class User(Entity):
    id: ID
    organization_siret: Siret
    email: str
    password_hash: str
    role: UserRole
    api_token: str

    def update_password(self, password_hash: str) -> None:
        self.password_hash = password_hash

    def update_api_token(self, api_token: str) -> None:
        self.api_token = api_token

    class Config:
        orm_mode = True
