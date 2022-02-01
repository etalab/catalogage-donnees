from server.domain.auth.entities import UserRole
from server.domain.common.types import ID
from server.seedwork.application.commands import Command


class CreateUser(Command[ID]):
    email: str
    role: UserRole = UserRole.USER


class DeleteUser(Command[None]):
    id: ID
