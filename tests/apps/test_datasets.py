import httpx
import pytest


@pytest.mark.asyncio
async def test_dataset_crud(client: httpx.AsyncClient) -> None:
    response = await client.post("/datasets/", json={"name": "Example"})
    assert response.status_code == 201
    data = response.json()
    pk = data["id"]
    assert isinstance(pk, int)
    assert data == {"id": pk, "name": "Example"}

    response = await client.get("/datasets/4242/")
    assert response.status_code == 404

    response = await client.get(f"/datasets/{pk}/")
    assert response.status_code == 200
    assert response.json() == {"id": pk, "name": "Example"}

    response = await client.get("/datasets/")
    assert response.status_code == 200
    assert response.json() == [{"id": pk, "name": "Example"}]
