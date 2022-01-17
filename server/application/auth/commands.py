from server.domain.common.types import ID
from server.seedwork.application.commands import Command


class CreateUser(Command[str]):
    email: str


class DeleteUser(Command[None]):
    id: ID
