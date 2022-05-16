from xpresso import Depends, FromJson, FromPath, HTTPException, Operation, Path

from server.application.auth.commands import CreateUser, DeleteUser
from server.application.auth.queries import GetUserByEmail, Login
from server.application.auth.views import AuthenticatedUserView, UserView
from server.config.di import resolve
from server.domain.auth.entities import UserRole
from server.domain.auth.exceptions import EmailAlreadyExists, LoginFailed
from server.domain.common.types import ID
from server.seedwork.application.messages import MessageBus

from .dependencies import HasRole, IsAuthenticated
from .schemas import CheckAuthResponse, UserCreate, UserLogin


async def create_user(data: FromJson[UserCreate]) -> UserView:
    bus = resolve(MessageBus)

    command = CreateUser(email=data.email, password=data.password)

    try:
        await bus.execute(command)
    except EmailAlreadyExists as exc:
        raise HTTPException(400, detail=str(exc))

    query = GetUserByEmail(email=data.email)
    return await bus.execute(query)


async def login(data: FromJson[UserLogin]) -> AuthenticatedUserView:
    bus = resolve(MessageBus)

    query = Login(email=data.email, password=data.password)

    try:
        return await bus.execute(query)
    except LoginFailed as exc:
        raise HTTPException(401, detail=str(exc))


async def delete_user(id: FromPath[ID]) -> None:
    bus = resolve(MessageBus)

    command = DeleteUser(id=id)
    await bus.execute(command)


async def check_auth() -> CheckAuthResponse:
    return CheckAuthResponse()


routes = [
    Path(
        "/users/",
        post=Operation(
            create_user,
            dependencies=[Depends(IsAuthenticated()), Depends(HasRole(UserRole.ADMIN))],
            response_status_code=201,
        ),
    ),
    Path("/login/", post=Operation(login)),
    Path(
        "/users/{id}/",
        delete=Operation(
            delete_user,
            dependencies=[Depends(IsAuthenticated()), Depends(HasRole(UserRole.ADMIN))],
            response_status_code=204,
        ),
    ),
    Path(
        "/check/",
        get=Operation(
            check_auth,
            dependencies=[Depends(IsAuthenticated())],
        ),
    ),
]
