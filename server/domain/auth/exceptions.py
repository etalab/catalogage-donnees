from ..common.exceptions import DoesNotExist


class UserDoesNotExist(DoesNotExist):
    entity_name = "User"


class EmailAlreadyExists(Exception):
    def __init__(self, email: str) -> None:
        super().__init__(f"Email already exists: {email!r}")
