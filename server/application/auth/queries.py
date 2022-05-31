from pydantic import EmailStr, SecretStr

from server.application.auth.views import AuthenticatedUserView, UserView
from server.seedwork.application.queries import Query


class Login(Query[AuthenticatedUserView]):
    email: EmailStr
    password: SecretStr


class GetUserByEmail(Query[UserView]):
    email: EmailStr


class GetUserByAPIToken(Query[UserView]):
    api_token: str
