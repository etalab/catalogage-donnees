import httpx
import pytest


@pytest.mark.asyncio
async def test_index(client: httpx.AsyncClient) -> None:
    response = await client.get("/")
    assert response.status_code == 307
    assert response.headers["Location"] == "/docs"
