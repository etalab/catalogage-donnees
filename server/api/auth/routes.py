from fastapi import APIRouter, Depends, HTTPException

from server.application.auth.commands import CreateUser, DeleteUser
from server.application.auth.queries import GetUserByEmail, Login
from server.application.auth.views import AuthenticatedUserView, UserView
from server.config.di import resolve
from server.domain.auth.entities import UserRole
from server.domain.auth.exceptions import EmailAlreadyExists, LoginFailed
from server.domain.common.types import ID
from server.seedwork.application.messages import MessageBus

from .permissions import HasRole, IsAuthenticated
from .schemas import CheckAuthResponse, UserCreate, UserLogin

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/users/",
    dependencies=[Depends(IsAuthenticated() & HasRole(UserRole.ADMIN))],
    response_model=UserView,
    status_code=201,
)
async def create_user(data: UserCreate) -> UserView:
    bus = resolve(MessageBus)

    command = CreateUser(email=data.email, password=data.password)

    try:
        await bus.execute(command)
    except EmailAlreadyExists as exc:
        raise HTTPException(400, detail=str(exc))

    query = GetUserByEmail(email=data.email)
    return await bus.execute(query)


@router.post("/login/", response_model=AuthenticatedUserView)
async def login(data: UserLogin) -> AuthenticatedUserView:
    bus = resolve(MessageBus)

    query = Login(email=data.email, password=data.password)

    try:
        return await bus.execute(query)
    except LoginFailed as exc:
        raise HTTPException(401, detail=str(exc))


@router.delete(
    "/users/{id}/",
    dependencies=[Depends(IsAuthenticated() & HasRole(UserRole.ADMIN))],
    status_code=204,
)
async def delete_user(id: ID) -> None:
    bus = resolve(MessageBus)

    command = DeleteUser(id=id)
    await bus.execute(command)


@router.get("/check/", dependencies=[Depends(IsAuthenticated())])
async def check_auth() -> CheckAuthResponse:
    return CheckAuthResponse()
