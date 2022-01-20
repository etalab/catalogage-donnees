import httpx
import pytest

from server.domain.common.types import id_factory


@pytest.mark.asyncio
async def test_dataset_crud(client: httpx.AsyncClient) -> None:
    response = await client.post("/datasets/", json={"name": "Example"})
    assert response.status_code == 201
    data = response.json()
    pk = data["id"]
    assert isinstance(pk, str)
    assert data == {"id": pk, "name": "Example"}

    response = await client.get(f"/datasets/{id_factory()}/")
    assert response.status_code == 404

    response = await client.get(f"/datasets/{pk}/")
    assert response.status_code == 200
    assert response.json() == {"id": pk, "name": "Example"}

    response = await client.get("/datasets/")
    assert response.status_code == 200
    assert response.json() == [{"id": pk, "name": "Example"}]

    response = await client.delete(f"/datasets/{pk}/")
    assert response.status_code == 204

    response = await client.get(f"/datasets/{pk}/")
    assert response.status_code == 404

    response = await client.get("/datasets/")
    assert response.status_code == 200
    assert response.json() == []
