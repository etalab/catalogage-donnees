import uuid
from typing import List, Optional, Tuple

from sqlalchemy import (
    Column,
    Computed,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    Integer,
    String,
    Table,
    desc,
    func,
    select,
    text,
)
from sqlalchemy.dialects.postgresql import ARRAY, TSVECTOR, UUID
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, relationship, selectinload

from server.domain.common.types import ID
from server.domain.datasets.entities import DataFormat, Dataset, UpdateFrequency
from server.domain.datasets.repositories import DatasetHeadlines, DatasetRepository

from ..database import Base, Database

# Association table
# See: https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html#many-to-many
dataset_dataformat = Table(
    "dataset_dataformat",
    Base.metadata,
    Column("dataset_id", ForeignKey("dataset.id"), primary_key=True),
    Column("dataformat_id", ForeignKey("dataformat.id"), primary_key=True),
)


class DataFormatModel(Base):
    __tablename__ = "dataformat"

    id = Column(Integer, primary_key=True)
    name = Column(Enum(DataFormat, name="dataformat_enum"), nullable=False, unique=True)
    datasets: List["DatasetModel"] = relationship(
        "DatasetModel",
        back_populates="formats",
        secondary=dataset_dataformat,
    )


class DatasetModel(Base):
    __tablename__ = "dataset"

    id: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True)
    created_at = Column(
        DateTime(timezone=True), server_default=func.clock_timestamp(), nullable=False
    )
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    formats: List[DataFormatModel] = relationship(
        "DataFormatModel",
        back_populates="datasets",
        secondary=dataset_dataformat,
    )
    entrypoint_email = Column(String, nullable=False)
    contact_emails = Column(ARRAY(String), server_default="{}", nullable=False)
    first_published_at = Column(DateTime(timezone=True))
    update_frequency = Column(Enum(UpdateFrequency, enum="update_frequency_enum"))
    last_updated_at = Column(DateTime(timezone=True))

    search_tsv: Mapped[str] = Column(
        TSVECTOR,
        Computed("to_tsvector('french', title || ' ' || description)", persisted=True),
    )

    __table_args__ = (
        Index(
            "ix_dataset_search_tsv",
            search_tsv,
            postgresql_using="GIN",
        ),
    )


def make_entity(instance: DatasetModel) -> Dataset:
    return Dataset(
        id=instance.id,
        created_at=instance.created_at,
        title=instance.title,
        description=instance.description,
        formats=[fmt.name for fmt in instance.formats],
        entrypoint_email=instance.entrypoint_email,
        contact_emails=instance.contact_emails,
        first_published_at=instance.first_published_at,
        update_frequency=instance.update_frequency,
        last_updated_at=instance.last_updated_at,
    )


def make_instance(entity: Dataset, formats: List[DataFormatModel]) -> DatasetModel:
    return DatasetModel(
        **entity.dict(
            exclude={
                "created_at",  # Managed by DB for better time consistency
                "formats",
            }
        ),
        formats=formats,
    )


def update_instance(
    instance: DatasetModel, entity: Dataset, formats: List[DataFormatModel]
) -> None:
    instance.title = entity.title
    instance.description = entity.description
    instance.formats = formats
    instance.entrypoint_email = entity.entrypoint_email
    instance.contact_emails = entity.contact_emails
    instance.first_published_at = entity.first_published_at
    instance.update_frequency = entity.update_frequency
    instance.last_updated_at = entity.last_updated_at


class SqlDatasetRepository(DatasetRepository):
    def __init__(self, db: Database) -> None:
        self._db = db

    async def get_all(self) -> List[Dataset]:
        async with self._db.session() as session:
            stmt = (
                select(DatasetModel)
                .options(selectinload(DatasetModel.formats))
                .order_by(DatasetModel.created_at.desc())
            )
            result = await session.execute(stmt)
            instances = result.scalars().all()
            return [make_entity(instance) for instance in instances]

    async def search(
        self, q: str, highlight: bool = False
    ) -> List[Tuple[Dataset, Optional[DatasetHeadlines]]]:
        async with self._db.session() as session:
            query_col = func.plainto_tsquery(text("'french'"), q)

            # 0 = (the default) ignores the document length
            # This is defined for the sake of being explicit:
            # * No need to normalize the `rank` value as we don't need it.
            # * Some normalization options allow penalizing longer documents, but this
            #   is irrelevant for our use cases (users may enter titles or descriptions
            #   as long as is necessary).
            # https://www.postgresql.org/docs/12/textsearch-controls.html#TEXTSEARCH-RANKING
            rank_normalization = 0

            rank_col = func.ts_rank_cd(
                DatasetModel.search_tsv, query_col, rank_normalization
            )

            title_headline_col = func.ts_headline(
                text("'french'"),
                DatasetModel.title,
                query_col,
                text("'StartSel=<mark>, StopSel=</mark>, HighlightAll=1'"),
            )

            description_headline_col = func.ts_headline(
                text("'french'"),
                DatasetModel.description,
                query_col,
                text("'StartSel=<mark>, StopSel=</mark>, MaxFragments=10'"),
            )

            headline_cols = (
                (title_headline_col, description_headline_col) if highlight else ()
            )

            stmt = (
                select(
                    DatasetModel,
                    rank_col.label("rank"),
                    *headline_cols,
                )
                .options(selectinload(DatasetModel.formats))
                .where(
                    # NOTE: SQLAlchemy has `.match(...)` that uses `to_tsquery()`.
                    # But we use this `.op()` advanced syntax because we need
                    # `plainto_tsquery()` to perform pre-processing and sanitization of
                    # the `q` user input for us (e.g. 'The Fat Rat' -> 'fat & rat').
                    # See:
                    # https://www.postgresql.org/docs/current/textsearch-controls.html
                    # https://docs.sqlalchemy.org/en/14/dialects/postgresql.html#full-text-search
                    DatasetModel.search_tsv.op("@@")(query_col)
                )
                .order_by(desc(text("rank")))
            )

            result = await session.execute(stmt)

            return [
                (
                    make_entity(instance),
                    {"title": headlines[0], "description": headlines[1]}
                    if headlines
                    else None,
                )
                for (instance, _, *headlines) in result
            ]

    async def _maybe_get_by_id(
        self, session: AsyncSession, id: ID
    ) -> Optional[DatasetModel]:
        stmt = (
            select(DatasetModel)
            .where(DatasetModel.id == id)
            .options(selectinload(DatasetModel.formats))
        )
        result = await session.execute(stmt)

        try:
            return result.scalar_one()
        except NoResultFound:
            return None

    async def get_by_id(self, id: ID) -> Optional[Dataset]:
        async with self._db.session() as session:
            instance = await self._maybe_get_by_id(session, id)

            if instance is None:
                return None

            return make_entity(instance)

    async def _get_formats(
        self, session: AsyncSession, formats: List[DataFormat]
    ) -> List[DataFormatModel]:
        stmt = select(DataFormatModel).where(DataFormatModel.name.in_(formats))
        result = await session.execute(stmt)
        return result.scalars().all()

    async def insert(self, entity: Dataset) -> ID:
        async with self._db.session() as session:
            formats = await self._get_formats(session, entity.formats)
            instance = make_instance(entity, formats)

            session.add(instance)

            await session.commit()
            await session.refresh(instance)

            return ID(instance.id)

    async def update(self, entity: Dataset) -> None:
        async with self._db.session() as session:
            instance = await self._maybe_get_by_id(session, entity.id)

            if instance is None:
                return

            formats = await self._get_formats(session, entity.formats)
            update_instance(instance, entity, formats)

            await session.commit()

    async def delete(self, id: ID) -> None:
        async with self._db.session() as session:
            instance = await self._maybe_get_by_id(session, id)

            if instance is None:
                return

            await session.delete(instance)

            await session.commit()
