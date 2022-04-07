from typing import Literal

from pydantic import BaseModel, EmailStr

from server.domain.auth.entities import UserRole
from server.domain.common.types import ID


class UserRead(BaseModel):
    id: ID
    email: str


class UserAuthenticatedRead(BaseModel):
    id: ID
    email: str
    role: UserRole
    api_token: str


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class CheckAuthResponse(BaseModel):
    is_authenticated: Literal[True] = True
