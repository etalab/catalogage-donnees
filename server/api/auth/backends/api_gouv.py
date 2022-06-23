from typing import Optional, Tuple

from authlib.integrations.starlette_client import OAuth
from fastapi import APIRouter
from starlette.authentication import AuthCredentials
from starlette.requests import HTTPConnection, Request
from starlette.responses import RedirectResponse, Response

from server.api.auth.models import ApiUser
from server.application.auth.views import UserView
from server.domain.auth.entities import UserRole
from server.domain.common.types import id_factory

from .base import AuthBackend


class ApiGouvAuthBackend(AuthBackend):
    """
    Authenticate users using the https://auth.api.gouv.fr OpenID Connect server.

    See: https://github.com/betagouv/api-auth
    """

    def router(self) -> APIRouter:
        router = APIRouter()

        # See: https://docs.authlib.org/en/latest/client/starlette.html#starlette-openid-connect  # noqa
        oauth = OAuth()

        oauth.register(
            name="api_gouv",
            client_id="client-id",  # TODO
            client_secret="client-secret",  # TODO
            server_metadata_url=(
                "https://auth.api.gouv.fr/.well-known/openid-configuration"
            ),
            client_kwargs={"scope": "openid email profile organizations"},
        )

        async def api_gouv_login(request: Request) -> Response:
            redirect_uri = request.url_for("api_gouv_callback")
            return await oauth.api_gouv.authorize_redirect(request, redirect_uri)

        async def api_gouv_callback(request: Request) -> Response:
            token = await oauth.api_gouv.authorize_access_token(request)
            request.session["api_gouv_userinfo"] = dict(token["userinfo"])
            return RedirectResponse("https://catalogue.multi.coop/")

        router.add_api_route("/auth/api_gouv/login", endpoint=api_gouv_login)
        router.add_api_route("/auth/api_gouv/callback", endpoint=api_gouv_callback)

        return router

    async def authenticate(
        self, conn: HTTPConnection
    ) -> Optional[Tuple[AuthCredentials, ApiUser]]:
        try:
            userinfo: dict = conn.session["api_gouv_userinfo"]
        except KeyError:
            return None

        obj = UserView(id=id_factory(), email=userinfo["email"], role=UserRole.USER)

        return AuthCredentials(scopes=["authenticated"]), ApiUser(obj)
