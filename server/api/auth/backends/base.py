from typing import Optional, Tuple

from fastapi import APIRouter
from starlette.authentication import AuthCredentials, AuthenticationBackend
from starlette.requests import HTTPConnection

from ..models import ApiUser


class AuthBackend(AuthenticationBackend):
    def get_openapi_security_definitions(self) -> dict:
        return {}

    def router(self) -> APIRouter:
        return APIRouter()

    async def authenticate(
        self, conn: HTTPConnection
    ) -> Optional[Tuple[AuthCredentials, ApiUser]]:
        """
        Authenticate a user associated with the current HTTP connection.

        Raises
        ------
        AuthenticationError:
            If authentication credentials were malformed or otherwise invalid.

        Returns
        -------
        An (AuthCredentials, ApiUser) tuple if authentication credentials were present
        and allowed to authenticate the user, None otherwise.

        See Also
        --------
        Starlette authentication guide: https://www.starlette.io/authentication/
        """
        raise NotImplementedError  # pragma: no cover
