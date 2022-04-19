from typing import Literal

from pydantic import BaseModel, EmailStr, SecretStr


class UserCreate(BaseModel):
    email: EmailStr
    password: SecretStr


class UserLogin(BaseModel):
    email: EmailStr
    password: SecretStr


class CheckAuthResponse(BaseModel):
    is_authenticated: Literal[True] = True
