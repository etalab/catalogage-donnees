from pydantic import SecretStr

from server.domain.common.types import ID
from server.seedwork.application.commands import Command


class CreateUser(Command[ID]):
    email: str
    password: SecretStr


class DeleteUser(Command[None]):
    id: ID
