from server.domain.common.types import ID
from server.seedwork.application.commands import Command


class CreateTag(Command[ID]):
    name: str
