from fastapi import HTTPException

from server.domain.auth.entities import UserRole

from ..types import APIRequest


class IsAuthenticated:
    def __call__(self, request: APIRequest) -> None:
        if not request.user.is_authenticated:
            raise HTTPException(401, detail="Invalid credentials")


class HasRole(IsAuthenticated):
    def __init__(self, *roles: UserRole) -> None:
        self._roles = roles

    def __call__(self, request: APIRequest) -> None:
        if not request.user.is_authenticated:
            raise RuntimeError(
                "Running HasRole but user is not authenticated. "
                "Hint: did you forget to add Depends(IsAuthenticated())?"
            )

        if request.user.obj.role not in self._roles:
            raise HTTPException(403, detail="Permission denied")
