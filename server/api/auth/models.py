from typing import Optional

from starlette.authentication import BaseUser

from server.application.auth.views import UserView


class ApiUser(BaseUser):
    def __init__(self, user: Optional[UserView]) -> None:
        self._user = user

    @property
    def obj(self) -> UserView:
        if self._user is None:
            raise RuntimeError(
                "Cannot access .obj, as the user is anonymous. "
                "Hint: did you forget to check for .is_authenticated?"
            )

        return self._user

    # Implement the 'BaseUser' interface.

    @property
    def is_authenticated(self) -> bool:
        return self._user is not None

    @property
    def display_name(self) -> str:
        return self._user.email if self._user is not None else ""
