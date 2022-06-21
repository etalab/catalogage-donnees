from typing import Optional, Tuple

from fastapi.encoders import jsonable_encoder
from fastapi.openapi.models import HTTPBearer
from starlette.authentication import AuthCredentials, AuthenticationError
from starlette.requests import HTTPConnection

from server.application.auth.queries import GetUserByAPIToken
from server.config.di import resolve
from server.domain.auth.exceptions import UserDoesNotExist
from server.seedwork.application.messages import MessageBus

from ..models import ApiUser
from .base import AuthBackend


class TokenAuthBackend(AuthBackend):
    """
    Authenticate users based on their API token: 'Authorization: Bearer <api_token>'
    """

    def get_openapi_security_definitions(self) -> dict:
        return {"Bearer": jsonable_encoder(HTTPBearer())}

    async def authenticate(
        self, conn: HTTPConnection
    ) -> Optional[Tuple[AuthCredentials, ApiUser]]:
        # NOTE: we don't reuse fastapi.security.HTTPBearer as it does not distinguish
        # "no Authorization" / "scheme is not Bearer" and "malformed Authorization".

        authorization = conn.headers.get("Authorization")

        if authorization is None:
            return None

        scheme, found, api_token = authorization.partition(" ")
        if not found:
            # Header is malformed -- that's a problem.
            raise AuthenticationError()

        if scheme.lower() != "bearer":
            return None

        bus = resolve(MessageBus)

        query = GetUserByAPIToken(api_token=api_token)

        try:
            user = await bus.execute(query)
        except UserDoesNotExist:
            raise AuthenticationError()

        return AuthCredentials(scopes=["authenticated"]), ApiUser(user)
