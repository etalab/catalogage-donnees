import httpx
import pytest

from server.api.app import App, create_app
from server.config.di import configure
from server.config.settings import Settings
from server.seedwork.application.di import Container

from .helpers import create_client


@pytest.mark.asyncio
async def test_debug_default_disabled(app: App, client: httpx.AsyncClient) -> None:
    assert not app.debug

    response = await client.get("/_debug_toolbar")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_debug_enabled(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("APP_DEBUG", "1")

    container = Container(configure)
    container.bootstrap()

    settings = container.resolve(Settings)
    app = create_app(settings)

    async with create_client(app) as client:
        response = await client.get("/_debug_toolbar")
        assert response.status_code != 404
