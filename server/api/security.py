from typing import Optional

from xpresso import Request


def get_bearer_token(request: Request) -> Optional[str]:
    try:
        authorization = request.headers["Authorization"]
    except KeyError:
        return None

    scheme, _, api_token = authorization.partition(" ")

    if not scheme or scheme.lower() != "bearer" or not api_token:
        return None

    return api_token
