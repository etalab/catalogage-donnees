from typing import Literal, Optional

import pydantic


class UserBase(pydantic.BaseModel):
    email: pydantic.EmailStr
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class TokenCreate(pydantic.BaseModel):
    email: str
    password: str


class TokenCreateResponse(pydantic.BaseModel):
    token: str


class CheckAuthResponse(pydantic.BaseModel):
    is_authenticated: Literal[True] = True
