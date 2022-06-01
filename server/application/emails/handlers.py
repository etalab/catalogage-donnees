from server.config.di import resolve
from server.domain.emails.backends import EmailBackend

from .commands import SendEmail


async def send_email(command: SendEmail) -> None:
    email_backend = resolve(EmailBackend)

    await email_backend.send(command.email)
