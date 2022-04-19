from pydantic import BaseModel

from server.domain.auth.entities import UserRole
from server.domain.common.types import ID


class UserView(BaseModel):
    id: ID
    email: str
    role: UserRole


class AuthenticatedUserView(BaseModel):
    id: ID
    email: str
    role: UserRole
    api_token: str
