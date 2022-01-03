from typing import Literal

import pydantic


class UserBase(pydantic.BaseModel):
    email: pydantic.EmailStr


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class CheckAuthResponse(pydantic.BaseModel):
    is_authenticated: Literal[True] = True
