from fastapi import Depends, HTTPException

from server.application.auth.queries import GetUserByEmail
from server.config.di import resolve
from server.domain.auth.entities import User
from server.domain.auth.exceptions import UserDoesNotExist
from server.seedwork.application.messages import MessageBus

from ..security import email_security


async def get_current_user(email: str = Depends(email_security)) -> User:
    bus = resolve(MessageBus)

    query = GetUserByEmail(email=email)

    try:
        return await bus.execute(query)
    except UserDoesNotExist:
        raise HTTPException(403, detail="Invalid credentials")
