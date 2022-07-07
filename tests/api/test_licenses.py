import httpx
import pytest

from server.config.di import resolve
from server.seedwork.application.messages import MessageBus

from ..factories import CreateDatasetFactory
from ..helpers import TestUser


@pytest.mark.asyncio
async def test_license_list(client: httpx.AsyncClient, temp_user: TestUser) -> None:
    bus = resolve(MessageBus)

    response = await client.get("/licenses/", auth=temp_user.auth)
    assert response.status_code == 200
    assert response.json() == ["Licence Ouverte", "ODC Open Database License"]

    await bus.execute(CreateDatasetFactory.build(license="Autre licence"))

    response = await client.get("/licenses/", auth=temp_user.auth)
    assert response.status_code == 200
    assert response.json() == [
        "Autre licence",
        "Licence Ouverte",
        "ODC Open Database License",
    ]


@pytest.mark.asyncio
async def test_license_list_permissions(client: httpx.AsyncClient) -> None:
    response = await client.get("/licenses/")
    assert response.status_code == 401
