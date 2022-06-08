from server.application.emails.commands import SendEmail
from server.application.emails.handlers import send_email
from server.seedwork.application.modules import Module


class EmailsModule(Module):
    command_handlers = {
        SendEmail: send_email,
    }

    query_handlers: dict = {}
