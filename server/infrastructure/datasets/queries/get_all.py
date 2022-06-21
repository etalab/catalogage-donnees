from typing import List

from sqlalchemy import desc, func, select, text
from sqlalchemy.engine import Row
from sqlalchemy.orm import contains_eager, selectinload
from sqlalchemy.sql import ColumnElement

from server.domain.datasets.repositories import DatasetGetAllExtras
from server.domain.datasets.specifications import DatasetSpec
from server.infrastructure.catalog_records.repositories import CatalogRecordModel
from server.infrastructure.tags.repositories import TagModel

from ..models import DatasetModel

_TS_HEADLINE_TITLE_COL = "ts_headline_title"
_TS_HEADLINE_DESCRIPTION_COL = "ts_headline_description"


class GetAllQuery:
    def __init__(self, spec: DatasetSpec) -> None:
        columns: List[ColumnElement] = []
        whereclauses = []
        orderbyclauses = []

        if (values := spec.geographical_coverage__in) is not None:
            whereclauses.append(
                DatasetModel.geographical_coverage.in_(values),
            )

        if (search_term := spec.search_term) is not None:
            # Search using a PostgreSQL text search vector (TSV).
            # See: https://www.postgresql.org/docs/12/textsearch-controls.html

            # Convert search term to normalized text search query.
            # E.g. 'Forêts françaises' -> 'forêt' & 'français'
            ts_query = func.plainto_tsquery(text("'french'"), search_term)

            # Compute search rank for each row
            # https://www.postgresql.org/docs/12/textsearch-controls.html#TEXTSEARCH-RANKING
            columns.append(
                func.ts_rank_cd(DatasetModel.search_tsv, ts_query).label("rank")
            )

            # Compute headlines (highlight markers) for title and description.
            # https://www.postgresql.org/docs/12/textsearch-controls.html#TEXTSEARCH-HEADLINE
            columns.append(
                func.ts_headline(
                    text("'french'"),
                    DatasetModel.title,
                    ts_query,
                    text("'StartSel=<mark>, StopSel=</mark>, HighlightAll=1'"),
                ).label(_TS_HEADLINE_TITLE_COL)
            )
            columns.append(
                func.ts_headline(
                    text("'french'"),
                    DatasetModel.description,
                    ts_query,
                    text("'StartSel=<mark>, StopSel=</mark>, MaxFragments=10'"),
                ).label(_TS_HEADLINE_DESCRIPTION_COL)
            )

            # Drop rows that don't match the search query.
            whereclauses.append(DatasetModel.search_tsv.op("@@")(ts_query))

            # Sort rows by search rank, best match first.
            orderbyclauses.append(desc(text("rank")))

        if (tag_ids := spec.tag__id__in) is not None:
            whereclauses.append(TagModel.id.in_(tag_ids))

        self.statement = (
            select(DatasetModel, *columns)
            .join(DatasetModel.catalog_record)
            .outerjoin(DatasetModel.tags)
            .options(
                selectinload(DatasetModel.formats),
                contains_eager(DatasetModel.catalog_record),
                contains_eager(DatasetModel.tags),
            )
            .where(*whereclauses)
            .order_by(*orderbyclauses, CatalogRecordModel.created_at.desc())
        )

    def instance(self, row: Row) -> DatasetModel:
        return row[0]

    def extras(self, row: Row) -> DatasetGetAllExtras:
        try:
            h_title = getattr(row, _TS_HEADLINE_TITLE_COL)
            h_description = getattr(row, _TS_HEADLINE_DESCRIPTION_COL)
        except AttributeError:
            return {}

        return {
            "headlines": {
                "title": h_title,
                "description": h_description if "<mark>" in h_description else None,
            }
        }
