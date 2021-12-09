import httpx
import pytest


@pytest.mark.asyncio
async def test_app(client: httpx.AsyncClient) -> None:
    response = await client.get("/")
    assert response.json() == {"message": "Hello, world!"}
