from server.domain.auth.entities import User
from server.seedwork.application.queries import Query


class GetUserByEmail(Query[User]):
    email: str
