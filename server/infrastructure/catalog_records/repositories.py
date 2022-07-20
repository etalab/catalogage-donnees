import datetime as dt
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Column, DateTime, func, select
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import relationship

from server.domain.catalog_records.entities import CatalogRecord
from server.domain.catalog_records.repositories import CatalogRecordRepository
from server.domain.common.types import ID

from ..database import Base, Database

if TYPE_CHECKING:
    from ..datasets.models import DatasetModel


class CatalogRecordModel(Base):
    __tablename__ = "catalog_record"

    id: ID = Column(UUID(as_uuid=True), primary_key=True)
    created_at: dt.datetime = Column(
        DateTime(timezone=True), server_default=func.clock_timestamp(), nullable=False
    )

    dataset: "DatasetModel" = relationship(
        "DatasetModel",
        back_populates="catalog_record",
        cascade="delete",
    )


def make_entity(instance: CatalogRecordModel) -> CatalogRecord:
    return CatalogRecord(
        id=instance.id,
        created_at=instance.created_at,
    )


def make_instance(entity: CatalogRecord) -> CatalogRecordModel:
    return CatalogRecordModel(
        **entity.dict(
            exclude={
                "created_at",  # Managed by DB for better time consistency
            }
        ),
    )


class SqlCatalogRecordRepository(CatalogRecordRepository):
    def __init__(self, db: Database) -> None:
        self._db = db

    async def get_by_id(self, id: ID) -> Optional[CatalogRecord]:
        async with self._db.session() as session:
            stmt = select(CatalogRecordModel).where(CatalogRecordModel.id == id)
            result = await session.execute(stmt)
            try:
                instance = result.scalar_one()
            except NoResultFound:
                return None
            else:
                return make_entity(instance)

    async def insert(self, entity: CatalogRecord) -> ID:
        async with self._db.session() as session:
            instance = make_instance(entity)

            session.add(instance)

            await session.commit()
            await session.refresh(instance)

            return ID(instance.id)
