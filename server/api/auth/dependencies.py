from fastapi import Depends, HTTPException
from fastapi.security.base import SecurityBase

from server.domain.auth.entities import UserRole

from ..resources import auth_backend
from ..types import APIRequest


class IsAuthenticated:
    """
    Require requests to be authenticated.

    Usage:
        @router.get(
            ...,
            dependencies=[
                Depends(IsAuthenticated()),
            ],
        )
    """

    def __call__(
        self,
        request: APIRequest,
        # Make FastAPI generated API docs register the security scheme,
        # and attach it to any route that has `Depends(IsAuthenticated())`.
        _: SecurityBase = Depends(auth_backend.security),
    ) -> None:
        if not request.user.is_authenticated:
            raise HTTPException(401, detail="Invalid credentials")


class HasRole:
    """
    An add-on to `IsAuthenticated()` which requires to authenticated user to
    have specific roles.

    Usage:

        @router.get(
            ...,
            dependencies=[
                Depends(IsAuthenticated()),
                Depends(HasRole(...)),
            ],
        )
    """

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
