from typing import List, Tuple

from sqlalchemy import desc, func, select, text
from sqlalchemy.ext.asyncio import AsyncResult
from sqlalchemy.orm import contains_eager, selectinload
from sqlalchemy.sql import ColumnElement, Select

from server.domain.datasets.entities import Dataset
from server.domain.datasets.repositories import DatasetGetAllExtras
from server.domain.datasets.specifications import DatasetSpec
from server.infrastructure.catalog_records.repositories import CatalogRecordModel

from ..models import DatasetModel
from ..transformers import make_entity


class GetAllQuery:
    def __init__(self, spec: DatasetSpec) -> None:
        self._spec = spec
        self._extra_columns: List[ColumnElement] = []
        self._whereclauses: List[ColumnElement] = []
        self._orderbyclauses: List[ColumnElement] = []
        self._ready = False

    def _prepare(self) -> None:
        assert not self._ready

        self._apply_geographical_coverage__in()
        self._apply_search()
        self._orderbyclauses.append(CatalogRecordModel.created_at.desc())

        self._ready = True

    def _apply_geographical_coverage__in(self) -> None:
        if self._spec.geographical_coverage__in is None:
            return

        self._whereclauses.append(
            DatasetModel.geographical_coverage.in_(self._spec.geographical_coverage__in)
        )

    def _apply_search(self) -> None:
        if self._spec.search is None:
            return

        query_col = func.plainto_tsquery(text("'french'"), self._spec.search.term)

        # No need to normalize the `rank` value as we don't need it.
        # https://www.postgresql.org/docs/12/textsearch-controls.html#TEXTSEARCH-RANKING
        rank_normalization = 0

        rank_col = func.ts_rank_cd(
            DatasetModel.search_tsv, query_col, rank_normalization
        )

        self._extra_columns.append(rank_col.label("rank"))
        self._whereclauses.append(DatasetModel.search_tsv.op("@@")(query_col))
        self._orderbyclauses.append(desc(text("rank")))

        if not self._spec.search.highlight:
            return

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

        self._extra_columns.extend((title_headline_col, description_headline_col))

    def statement(self) -> Select:
        self._prepare()

        return (
            select(DatasetModel, *self._extra_columns)
            .join(DatasetModel.catalog_record)
            .options(
                selectinload(DatasetModel.formats),
                selectinload(DatasetModel.tags),
                contains_eager(DatasetModel.catalog_record),
            )
            .where(*self._whereclauses)
            .order_by(*self._orderbyclauses)
        )

    def _make_extras(self, extra_values: list) -> DatasetGetAllExtras:
        try:
            _, *headline_values = extra_values
        except ValueError:
            return {}

        try:
            htitle, hdescription = headline_values
        except ValueError:
            return {}

        return {
            "headlines": {
                "title": htitle,
                "description": hdescription if "<mark>" in hdescription else None,
            }
        }

    async def gather(
        self, result: AsyncResult
    ) -> List[Tuple[Dataset, DatasetGetAllExtras]]:
        return [
            (make_entity(instance), self._make_extras(extra_values))
            async for instance, *extra_values in result
        ]
