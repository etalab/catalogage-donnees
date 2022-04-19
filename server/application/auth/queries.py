from pydantic import SecretStr

from server.application.auth.views import AuthenticatedUserView, UserView
from server.seedwork.application.queries import Query


class Login(Query[AuthenticatedUserView]):
    email: str
    password: SecretStr


class GetUserByEmail(Query[UserView]):
    email: str


class GetUserByAPIToken(Query[UserView]):
    api_token: str
