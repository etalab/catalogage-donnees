from starlette.requests import Request

from .auth.models import ApiUser


class APIRequest(Request):
    user: ApiUser  # Set by AuthMiddleware.
