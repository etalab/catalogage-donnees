from typing import List

from server.domain.common.types import ID
from server.domain.datasets.entities import DataFormat
from server.seedwork.application.commands import Command


class CreateDataset(Command[ID]):
    title: str
    description: str
    formats: List[DataFormat]


class UpdateDataset(Command[None]):
    id: ID
    title: str
    description: str
    formats: List[DataFormat]


class DeleteDataset(Command[None]):
    id: ID
