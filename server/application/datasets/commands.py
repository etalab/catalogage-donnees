from typing import List

from pydantic import Field

from server.domain.common.types import ID
from server.domain.datasets.entities import DataFormat
from server.seedwork.application.commands import Command


class CreateDataset(Command[ID]):
    title: str
    description: str
    formats: List[DataFormat]
    entrypoint_email: str
    contact_emails: List[str] = Field(default_factory=list)


class UpdateDataset(Command[None]):
    id: ID
    title: str
    description: str
    formats: List[DataFormat]
    entrypoint_email: str
    contact_emails: List[str]


class DeleteDataset(Command[None]):
    id: ID
