from typing import List

import httpx
import pytest
from pydantic import SecretStr

from server.application.emails.commands import SendEmail
from server.config.di import resolve
from server.domain.emails.entities import Email
from server.domain.emails.exceptions import EmailDeliveryFailed
from server.infrastructure.emails.backends.console import ConsoleEmailBackend
from server.infrastructure.emails.backends.mailpace import MailPaceEmailBackend
from server.seedwork.application.messages import MessageBus

from ..mocks.email import outbox

EMAIL = Email(
    subject="Test subject",
    from_email="test-from@mydomain.org",
    recipients=["recipient1@mydomain.org", "recipient2@mydomain.org"],
    body="This is a test email.",
)


@pytest.mark.asyncio
async def test_send_email() -> None:
    bus = resolve(MessageBus)

    await bus.execute(SendEmail(email=EMAIL))

    assert len(outbox) == 1
    emails = outbox.all()
    assert emails == [EMAIL]


@pytest.mark.asyncio
async def test_console_backend(capsys: pytest.CaptureFixture) -> None:
    backend = ConsoleEmailBackend()

    await backend.send(EMAIL)

    out = capsys.readouterr().out
    assert f"Subject: {EMAIL.subject}\r\n" in out


@pytest.mark.asyncio
async def test_mailpace_backend() -> None:
    requests: List[httpx.Request] = []

    async def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.host == "app.mailpace.com"
        requests.append(request)
        return httpx.Response(200, json={"id": 123, "status": "pending"})

    mounts = {"all://*mailpace.com": httpx.MockTransport(handler)}

    async with httpx.AsyncClient(mounts=mounts) as client:
        backend = MailPaceEmailBackend(client=client, api_token=SecretStr("<testing>"))

        await backend.send(EMAIL)

        assert len(requests) == 1
        (request,) = requests
        # Ensure request complies with: https://docs.mailpace.com/reference/send
        assert request.method == "POST"
        assert str(request.url) == "https://app.mailpace.com/api/v1/send"
        assert "application/json" in request.headers["Accept"]
        assert request.headers["Content-Type"] == "application/json"
        assert request.headers["MailPace-Server-Token"] == "<testing>"


@pytest.mark.asyncio
async def test_mailpace_backend_handles_server_errors() -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.host == "app.mailpace.com"
        return httpx.Response(500)

    mounts = {"all://*mailpace.com": httpx.MockTransport(handler)}

    async with httpx.AsyncClient(mounts=mounts) as client:
        backend = MailPaceEmailBackend(client=client, api_token=SecretStr("<testing>"))

        with pytest.raises(EmailDeliveryFailed, match="<No Content>"):
            await backend.send(EMAIL)


@pytest.mark.asyncio
async def test_mailpace_backend_handles_client_errors() -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.host == "app.mailpace.com"
        return httpx.Response(400, json={"error": "Invalid API Token"})

    mounts = {"all://*mailpace.com": httpx.MockTransport(handler)}

    async with httpx.AsyncClient(mounts=mounts) as client:
        backend = MailPaceEmailBackend(client=client, api_token=SecretStr("<testing>"))

        with pytest.raises(EmailDeliveryFailed, match="Invalid API Token"):
            await backend.send(EMAIL)
