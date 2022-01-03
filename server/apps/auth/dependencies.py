from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from server.db import get_db

from . import queries
from .models import User
from .security import bearer_security


async def get_current_user(
    db: AsyncSession = Depends(get_db),
    authorization: HTTPAuthorizationCredentials = Depends(bearer_security),
) -> User:
    token = await queries.get_token(db, key=authorization.credentials)

    if token is None:
        raise HTTPException(403, detail="Invalid credentials")

    return token.user
