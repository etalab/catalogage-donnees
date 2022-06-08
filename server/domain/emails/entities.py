from email.utils import make_msgid
from typing import List

from pydantic import BaseModel, Field


class Email(BaseModel):
    subject: str
    from_email: str
    recipients: List[str]
    body: str
    msgid: str = Field(default_factory=make_msgid)
