import httpx

from server.domain.auth.entities import User


def authenticate(request: httpx.Request, user: User) -> None:
    """
    Authenticate a test HTTP request, using the server-accepted authentication method.
    """
    request.headers["X-Email"] = user.email
