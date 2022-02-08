from server.domain.common.types import ID
from server.seedwork.application.commands import Command


class CreateDataset(Command[ID]):
    title: str
    description: str


class UpdateDataset(Command[None]):
    id: ID
    title: str
    description: str


class DeleteDataset(Command[None]):
    id: ID
