from typing import Tuple

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select

from server.domain.common.pagination import Page


def to_limit_offset(page: Page) -> Tuple[int, int]:
    limit = page.size
    offset = page.size * (page.number - 1)
    return limit, offset


async def get_count_from(stmt: Select, session: AsyncSession) -> int:
    count_stmt = select(func.count()).select_from(stmt.subquery())
    result = await session.execute(count_stmt)
    return result.scalar_one()
