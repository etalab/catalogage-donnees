import json
from typing import Any

from fastapi.encoders import jsonable_encoder
from sqlalchemy import cast, delete, func, insert, literal, select
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.asyncio import AsyncSession

from server.domain.common.types import id_factory

from .models import DeletedRecordModel


async def soft_delete(session: AsyncSession, instance: Any) -> None:
    model = type(instance)

    await _soft_delete_tablelike(
        session,
        model,
        table_name=model.__tablename__,
        where=model.id == instance.id,
        pk_jsonb={"id": instance.id},
    )


async def soft_delete_table(
    session: AsyncSession,
    table: Any,
    where: Any,
    pk_jsonb: Any,
) -> None:
    await _soft_delete_tablelike(
        session,
        table,
        table_name=table.name,
        where=where,
        pk_jsonb=pk_jsonb,
    )


async def _soft_delete_tablelike(
    session: AsyncSession,
    tablelike: Any,
    table_name: str,
    where: Any,
    pk_jsonb: Any,
) -> None:
    # Prefer soft-deleting by moving rows to an archival table, to avoid pitfalls and
    # drawbacks of the more common "deleted_at = now()" style.
    #
    # This style:
    # * Does not pollute tables with a `.deleted_at` column or queries with a
    #  `WHERE deleted_at is NULL` check.
    # * Enforces foreign keys: soft-deleting without deleting related rows beforehand
    #   is an error.
    # * Allows physical deletion by deleting a time window of deleted records.
    #
    # See: https://brandur.org/soft-deletion
    # See: https://news.ycombinator.com/item?id=32156009
    # See "Conclusion" here: https://blog.miguelgrinberg.com/post/implementing-the-soft-delete-pattern-with-flask-and-sqlalchemy  # noqa: E501

    deleted_cte = delete(tablelike).where(where).returning(tablelike).cte("deleted_cte")

    upsert = insert(DeletedRecordModel).from_select(
        ["id", "original_table", "original_pk", "data"],
        select(
            literal(id_factory()),
            literal(table_name),
            cast(literal(json.dumps(jsonable_encoder(pk_jsonb))), JSONB),
            func.to_jsonb(deleted_cte.table_valued()),
        ),
    )

    await session.execute(upsert)
