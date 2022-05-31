from pydantic import EmailStr, SecretStr

from server.domain.common.types import ID
from server.seedwork.application.commands import Command


class CreateUser(Command[ID]):
    email: EmailStr
    password: SecretStr


class DeleteUser(Command[None]):
    id: ID


class ChangePassword(Command[None]):
    email: EmailStr
    password: SecretStr
