import json

import httpx
from pydantic import SecretStr

from server.config.di import resolve
from server.config.settings import Settings
from server.domain.emails.backends import EmailBackend
from server.domain.emails.entities import Email
from server.domain.emails.exceptions import EmailDeliveryFailed


class MailPaceEmailBackend(EmailBackend):
    """
    Send emails via the MailPace HTTPS API.

    See: https://docs.mailpace.com/
    """

    def __init__(
        self, *, client: httpx.AsyncClient = None, api_token: SecretStr
    ) -> None:
        if client is None:
            client = httpx.AsyncClient()

        self._client = client
        self._api_token = api_token

    @classmethod
    def options(self) -> dict:
        settings = resolve(Settings)
        assert settings.mailpace_api_token is not None
        return {"api_token": settings.mailpace_api_token}

    async def send(self, email: Email, fail_silently: bool = False) -> bool:
        payload = {
            "from": email.from_email,
            "to": ", ".join(email.recipients),
            "subject": email.subject,
            "textbody": email.body,
        }

        request = httpx.Request(
            method="POST",
            url="https://app.mailpace.com/api/v1/send",
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "MailPace-Server-Token": self._api_token.get_secret_value(),
            },
            json=payload,
        )

        response = await self._client.send(request)

        try:
            response.raise_for_status()
        except httpx.HTTPStatusError:
            try:
                message = response.json()
            except json.JSONDecodeError:
                message = "<Invalid JSON>" if response.text else "<No Content>"

            # TODO: log an error message

            if fail_silently:
                return False

            raise EmailDeliveryFailed(message)

        return True
