import enum

from server.seedwork.domain.entities import Entity

from ..common.types import ID


class UserRole(enum.Enum):
    USER = "USER"
    ADMIN = "ADMIN"


class User(Entity):
    id: ID
    email: str
    password_hash: str
    role: UserRole
    api_token: str

    class Config:
        orm_mode = True
