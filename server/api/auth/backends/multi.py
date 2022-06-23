from typing import Optional, Sequence, Tuple

from fastapi import APIRouter
from starlette.authentication import AuthCredentials, AuthenticationError
from starlette.requests import HTTPConnection

from ..models import ApiUser
from .base import AuthBackend


class MultiAuthBackend(AuthBackend):
    """
    An authentication backend that runs through a series of auth backends until
    one successfully authenticates the user.
    """

    def __init__(self, backends: Sequence[AuthBackend]) -> None:
        self._backends = backends

    def get_openapi_security_definitions(self) -> dict:
        definitions = {}
        for backend in self._backends:
            definitions.update(backend.get_openapi_security_definitions())
        return definitions

    def router(self) -> APIRouter:
        router = APIRouter()
        for backend in self._backends:
            router.include_router(backend.router())
        return router

    async def authenticate(
        self, conn: HTTPConnection
    ) -> Optional[Tuple[AuthCredentials, ApiUser]]:
        for backend in self._backends:
            try:
                auth = await backend.authenticate(conn)
            except AuthenticationError:
                raise  # Propagate authentication errors.

            if auth is not None:
                return auth

        return None
