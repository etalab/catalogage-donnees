from typing import List, Optional, Tuple

from sqlalchemy import desc, func, select, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from server.domain.common.pagination import Page
from server.domain.common.types import ID
from server.domain.datasets.entities import DataFormat, Dataset
from server.domain.datasets.repositories import (
    DatasetHeadlines,
    DatasetRepository,
    SearchResult,
)
from server.domain.datasets.specifications import DatasetSpec
from server.domain.tags.entities import Tag

from ..catalog_records.repositories import CatalogRecordModel
from ..database import Database
from ..helpers.sqlalchemy import get_count_from, to_limit_offset
from ..tags.repositories import TagModel
from .models import DataFormatModel, DatasetModel
from .transformers import make_entity, make_instance, update_instance


class SqlDatasetRepository(DatasetRepository):
    def __init__(self, db: Database) -> None:
        self._db = db

    async def get_all(
        self,
        *,
        page: Page = Page(),
        spec: DatasetSpec = DatasetSpec(),
    ) -> Tuple[List[Dataset], int]:
        limit, offset = to_limit_offset(page)

        async with self._db.session() as session:
            stmt = (
                select(DatasetModel)
                .options(
                    selectinload(DatasetModel.formats),
                    selectinload(DatasetModel.tags),
                )
                .join(DatasetModel.catalog_record)
            )

            if spec.geographical_coverage__in is not None:
                stmt = stmt.where(
                    DatasetModel.geographical_coverage.in_(
                        spec.geographical_coverage__in
                    )
                )

            stmt = stmt.order_by(CatalogRecordModel.created_at.desc())

            count = await get_count_from(stmt, session)
            result = await session.execute(stmt.limit(limit).offset(offset))
            instances = result.scalars().all()
            items = [make_entity(instance) for instance in instances]
            return items, count

    async def search(
        self,
        q: str,
        highlight: bool = False,
        page: Page = Page(),
    ) -> Tuple[List[SearchResult], int]:
        limit, offset = to_limit_offset(page)

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
                .options(
                    selectinload(DatasetModel.formats),
                    selectinload(DatasetModel.tags),
                )
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

            count = await get_count_from(stmt, session)

            result = await session.execute(stmt.limit(limit).offset(offset))

            def _make_headlines(values: list) -> DatasetHeadlines:
                htitle, hdescription = values
                return {
                    "title": htitle,
                    "description": hdescription if "<mark>" in hdescription else None,
                }

            items: List[SearchResult] = [
                (
                    make_entity(instance),
                    _make_headlines(headline_values) if headline_values else None,
                )
                for instance, _, *headline_values in result
            ]

            return items, count

    async def _maybe_get_by_id(
        self, session: AsyncSession, id: ID
    ) -> Optional[DatasetModel]:
        stmt = (
            select(DatasetModel)
            .where(DatasetModel.id == id)
            .options(
                selectinload(DatasetModel.formats),
                selectinload(DatasetModel.tags),
            )
        )
        result = await session.execute(stmt)

        return result.scalar_one_or_none()

    async def get_by_id(self, id: ID) -> Optional[Dataset]:
        async with self._db.session() as session:
            instance = await self._maybe_get_by_id(session, id)

            if instance is None:
                return None

            return make_entity(instance)

    async def _get_catalog_record(
        self, session: AsyncSession, id_: ID
    ) -> CatalogRecordModel:
        stmt = select(CatalogRecordModel).where(CatalogRecordModel.id == id_)
        result = await session.execute(stmt)
        return result.scalar_one()

    async def _get_formats(
        self, session: AsyncSession, formats: List[DataFormat]
    ) -> List[DataFormatModel]:
        stmt = select(DataFormatModel).where(DataFormatModel.name.in_(formats))
        result = await session.execute(stmt)
        return result.scalars().all()

    async def _get_tags(self, session: AsyncSession, tags: List[Tag]) -> List[TagModel]:
        stmt = select(TagModel).where(TagModel.id.in_({tag.id for tag in tags}))
        result = await session.execute(stmt)
        return result.scalars().all()

    async def insert(self, entity: Dataset) -> ID:
        async with self._db.session() as session:
            async with session.begin():
                catalog_record = await self._get_catalog_record(
                    session, entity.catalog_record.id
                )
                formats = await self._get_formats(session, entity.formats)
                tags = await self._get_tags(session, entity.tags)
                instance = make_instance(entity, catalog_record, formats, tags)

                session.add(instance)

            await session.refresh(instance)

            return ID(instance.id)

    async def update(self, entity: Dataset) -> None:
        async with self._db.session() as session:
            async with session.begin():
                instance = await self._maybe_get_by_id(session, entity.id)

                if instance is None:
                    return

                formats = await self._get_formats(session, entity.formats)
                tags = await self._get_tags(session, entity.tags)
                update_instance(instance, entity, formats, tags)

    async def delete(self, id: ID) -> None:
        async with self._db.session() as session:
            instance = await self._maybe_get_by_id(session, id)

            if instance is None:
                return

            await session.delete(instance)

            await session.commit()
