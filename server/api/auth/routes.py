from fastapi import APIRouter, Depends, HTTPException

from server.application.auth.commands import CreateUser, DeleteUser
from server.application.auth.queries import GetUserByEmail
from server.config.di import resolve
from server.domain.auth.entities import User
from server.domain.auth.exceptions import EmailAlreadyExists
from server.domain.common.types import ID
from server.seedwork.application.messages import MessageBus

from .dependencies import get_current_user
from .schemas import CheckAuthResponse, UserCreate, UserRead

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/users/", response_model=UserRead, status_code=201)
async def create_user(data: UserCreate) -> User:
    bus = resolve(MessageBus)

    command = CreateUser(email=data.email)

    try:
        await bus.execute(command)
    except EmailAlreadyExists as exc:
        raise HTTPException(400, detail=str(exc))

    query = GetUserByEmail(email=data.email)
    return await bus.execute(query)


@router.delete("/users/{id}/", status_code=204)
async def delete_user(id: ID) -> None:
    bus = resolve(MessageBus)

    command = DeleteUser(id=id)
    await bus.execute(command)


@router.get("/check/")
async def check_auth(_: User = Depends(get_current_user)) -> CheckAuthResponse:
    return CheckAuthResponse()
