from typing import List

from server.domain.emails.backends import EmailBackend
from server.domain.emails.entities import Email


class _EmailOutbox:
    def __init__(self) -> None:
        self._emails: List[Email] = []

    def __len__(self) -> int:
        return len(self._emails)

    def add(self, email: Email) -> None:
        self._emails.append(email)

    def all(self) -> List[Email]:
        return list(self._emails)

    def clear(self) -> None:
        self._emails.clear()


_OUTBOX = _EmailOutbox()


class TestingEmailBackend(EmailBackend):
    """
    Record emails to an in-memory outbox.
    """

    async def send(self, email: Email, fail_silently: bool = False) -> bool:
        _OUTBOX.add(email)
        return True


outbox = _OUTBOX
