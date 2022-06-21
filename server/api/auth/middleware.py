from typing import Optional, Tuple

from starlette.authentication import AuthCredentials, AuthenticationBackend
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.requests import HTTPConnection
from starlette.responses import JSONResponse, Response
from starlette.types import ASGIApp

from .backends.base import AuthBackend
from .models import ApiUser


class AuthMiddleware(AuthenticationMiddleware):
    def __init__(self, app: ASGIApp, backend: AuthBackend) -> None:
        super().__init__(app, backend=_BackendWrapper(backend))

    @staticmethod
    def default_on_error(conn: HTTPConnection, exc: Exception) -> Response:
        return JSONResponse({"detail": "Invalid credentials"}, status_code=401)


class _BackendWrapper(AuthenticationBackend):
    def __init__(self, backend: AuthBackend) -> None:
        self._backend = backend

    async def authenticate(
        self, conn: HTTPConnection
    ) -> Optional[Tuple[AuthCredentials, ApiUser]]:
        auth = await self._backend.authenticate(conn)

        if auth is None:
            # Provide a default which implements our ApiUser interface.
            # (Starlette's 'AuthenticationMiddleware' would default to
            # 'starlette.authentication.UnauthenticatedUser'.)
            return AuthCredentials(), ApiUser(None)

        return auth
