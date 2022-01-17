import enum

from server.seedwork.domain.entities import Entity

from ..common.types import ID


class UserRole(enum.Enum):
    USER = "USER"
    ADMIN = "ADMIN"


class User(Entity):
    id: ID
    email: str
    role: UserRole

    class Config:
        orm_mode = True
