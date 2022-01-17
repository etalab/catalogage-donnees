from fastapi import Depends, HTTPException

from server.domain.auth.entities import User, UserRole

from .dependencies import get_current_user


class IsAuthenticated:
    async def __call__(self, _: User = Depends(get_current_user)) -> None:
        pass


class HasRole:
    def __init__(self, *roles: UserRole) -> None:
        self.roles = roles

    def __call__(self, user: User = Depends(get_current_user)) -> None:
        if user.role not in self.roles:
            raise HTTPException(403, detail="Permission denied")
