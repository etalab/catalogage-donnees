from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from . import passwords, queries
from .models import User


async def authenticate(db: AsyncSession, email: str, password: str) -> Optional[User]:
    user = await queries.get_user_by_email(db, email=email)

    if user is None:
        # Hash the password in this case as well, to mitigate timing attacks.
        # See: https://code.djangoproject.com/ticket/20760
        _ = passwords.hash(password)
        return None

    if not user.check_password(password):
        return None

    return user
