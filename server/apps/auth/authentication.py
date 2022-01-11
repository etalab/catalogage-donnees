from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from . import queries
from .models import User


async def authenticate(db: AsyncSession, email: str) -> Optional[User]:
    return await queries.get_user_by_email(db, email=email)
