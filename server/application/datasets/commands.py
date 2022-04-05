import datetime as dt
from typing import List, Optional

from pydantic import Field

from server.domain.common.types import ID
from server.domain.datasets.entities import DataFormat, UpdateFrequency
from server.seedwork.application.commands import Command


class CreateDataset(Command[ID]):
    title: str
    description: str
    formats: List[DataFormat]
    service: str
    entrypoint_email: str
    contact_emails: List[str] = Field(default_factory=list)
    first_published_at: Optional[dt.datetime] = None
    update_frequency: Optional[UpdateFrequency] = None
    last_updated_at: Optional[dt.datetime] = None


class UpdateDataset(Command[None]):
    id: ID
    title: str
    description: str
    formats: List[DataFormat]
    service: str
    entrypoint_email: str
    contact_emails: List[str]
    first_published_at: Optional[dt.datetime] = Field(...)
    update_frequency: Optional[UpdateFrequency] = Field(...)
    last_updated_at: Optional[dt.datetime] = Field(...)


class DeleteDataset(Command[None]):
    id: ID
