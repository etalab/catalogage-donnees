from server.domain.emails.entities import Email
from server.seedwork.application.commands import Command


class SendEmail(Command[None]):
    email: Email
