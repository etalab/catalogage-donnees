import sys
from email.message import EmailMessage
from email.policy import SMTPUTF8
from email.utils import formatdate
from typing import TextIO

from server.domain.emails.backends import EmailBackend
from server.domain.emails.entities import Email


class ConsoleEmailBackend(EmailBackend):
    """
    Log emails to the console.
    """

    def __init__(self, stream: TextIO = None) -> None:
        if stream is None:
            stream = sys.stdout

        self._stream = stream

    async def send(self, email: Email, fail_silently: bool = False) -> bool:
        message = EmailMessage(SMTPUTF8)
        message.set_charset("utf-8")

        message["Subject"] = email.subject
        message["From"] = email.from_email
        message["To"] = ", ".join(email.recipients)
        message["Date"] = formatdate(localtime=True)
        message["Message-ID"] = email.msgid
        message.set_payload(email.body, "utf-8")

        content = message.as_bytes().decode("utf-8")
        self._stream.write(f"{content}\n{78 * '-'}\n")

        return True
