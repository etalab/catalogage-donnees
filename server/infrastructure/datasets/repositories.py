import uuid
from typing import List, Optional

from sqlalchemy import Column, String, delete, insert, select, update
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.exc import NoResultFound

from server.domain.common.types import ID
from server.domain.datasets.entities import Dataset
from server.domain.datasets.repositories import DatasetRepository

from ..database import Base, Database


class DatasetModel(Base):
    __tablename__ = "dataset"

    id: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)


class SqlDatasetRepository(DatasetRepository):
    def __init__(self, db: Database) -> None:
        self._db = db

    async def get_all(self) -> List[Dataset]:
        async with self._db.session() as session:
            stmt = select(DatasetModel)
            result = await session.execute(stmt)
            objs = result.scalars().all()
            return [Dataset.from_orm(obj) for obj in objs]

    async def get_by_id(self, id: ID) -> Optional[Dataset]:
        async with self._db.session() as session:
            stmt = select(DatasetModel).where(DatasetModel.id == id)
            result = await session.execute(stmt)
            try:
                obj = result.scalar_one()
            except NoResultFound:
                return None
            else:
                return Dataset.from_orm(obj)

    async def insert(self, entity: Dataset) -> ID:
        async with self._db.session() as session:
            stmt = (
                insert(DatasetModel).values(**entity.dict()).returning(DatasetModel.id)
            )
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar_one()

    async def update(self, entity: Dataset) -> None:
        async with self._db.session() as session:
            stmt = (
                update(DatasetModel)
                .where(DatasetModel.id == entity.id)
                .values(**entity.dict(exclude={"id"}))
            )
            await session.execute(stmt)
            await session.commit()

    async def delete(self, id: ID) -> None:
        async with self._db.session() as session:
            stmt = delete(DatasetModel).where(DatasetModel.id == id)
            await session.execute(stmt)
            await session.commit()
