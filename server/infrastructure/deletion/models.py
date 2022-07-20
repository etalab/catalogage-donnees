import datetime as dt
import uuid

from sqlalchemy import Column, DateTime, String, func
from sqlalchemy.dialects.postgresql import JSONB, UUID

from ..database import Base


class DeletedRecordModel(Base):
    """
    A table of deleted records, for archival, auditing and troubleshooting purposes.
    """

    __tablename__ = "deleted_record"

    id: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True)
    deleted_at: dt.datetime = Column(
        DateTime(timezone=True), server_default=func.clock_timestamp(), nullable=False
    )
    original_table = Column(String(), nullable=False)
    original_pk: dict = Column(JSONB(), nullable=False)
    data: dict = Column(JSONB(), nullable=False)
