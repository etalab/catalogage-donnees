from pydantic import SecretStr

from server.domain.auth.entities import User
from server.seedwork.application.queries import Query


class Login(Query[User]):
    email: str
    password: SecretStr


class GetUserByEmail(Query[User]):
    email: str


class GetUserByAPIToken(Query[User]):
    api_token: str
