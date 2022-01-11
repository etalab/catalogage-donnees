from server.domain.common.types import ID
from server.seedwork.application.commands import Command


class CreateDataset(Command[ID]):
    name: str


class DeleteDataset(Command[None]):
    id: ID
