from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from server.db import get_db

from .authentication import authenticate
from .models import User
from .security import email_security


async def get_current_user(
    db: AsyncSession = Depends(get_db),
    email: str = Depends(email_security),
) -> User:
    user = await authenticate(db, email)

    if user is None:
        raise HTTPException(403, detail="Invalid credentials")

    return user
