from typing import Optional

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials

from server.application.auth.queries import GetUserByAPIToken
from server.config.di import resolve
from server.domain.auth.entities import User
from server.domain.auth.exceptions import UserDoesNotExist
from server.seedwork.application.messages import MessageBus

from ..security import bearer_security


async def current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_security),
) -> User:
    if credentials is None:
        raise HTTPException(401, detail="Invalid credentials")

    bus = resolve(MessageBus)

    query = GetUserByAPIToken(api_token=credentials.credentials)

    try:
        return await bus.execute(query)
    except UserDoesNotExist:
        raise HTTPException(401, detail="Invalid credentials")
