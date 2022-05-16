from typing import Optional

from starlette.exceptions import HTTPException
from xpresso import Depends
from xpresso.typing import Annotated

from server.application.auth.queries import GetUserByAPIToken
from server.config.di import resolve
from server.domain.auth.entities import User, UserRole
from server.domain.auth.exceptions import UserDoesNotExist
from server.seedwork.application.messages import MessageBus

from ..security import get_bearer_token


async def current_user(
    api_token: Annotated[Optional[str], Depends(get_bearer_token)]
) -> User:
    if api_token is None:
        raise HTTPException(401, detail="Invalid credentials")

    bus = resolve(MessageBus)

    query = GetUserByAPIToken(api_token=api_token)

    try:
        return await bus.execute(query)
    except UserDoesNotExist:
        raise HTTPException(401, detail="Invalid credentials")


CurrentUser = Annotated[User, Depends(current_user)]


class IsAuthenticated:
    def __call__(self, _: CurrentUser) -> None:
        pass


class HasRole:
    def __init__(self, *roles: UserRole) -> None:
        self._roles = frozenset(roles)

    def __call__(self, user: CurrentUser) -> None:
        if user.role not in self._roles:
            raise HTTPException(403, detail="Permission denied")
