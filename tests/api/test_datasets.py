import httpx
import pytest


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "payload, expected_errors_attrs",
    [
        pytest.param(
            {},
            [
                {"loc": ["body", "title"], "type": "value_error.missing"},
                {"loc": ["body", "description"], "type": "value_error.missing"},
            ],
            id="missing-fields",
        ),
    ],
)
async def test_create_dataset_invalid(
    client: httpx.AsyncClient, payload: dict, expected_errors_attrs: list
) -> None:
    response = await client.post("/datasets/", json=payload)
    assert response.status_code == 422

    data = response.json()
    assert len(data["detail"]) == len(expected_errors_attrs)

    for error, expected_error_attrs in zip(data["detail"], expected_errors_attrs):
        error_attrs = {key: error[key] for key in expected_error_attrs}
        assert error_attrs == expected_error_attrs


@pytest.mark.asyncio
async def test_create_dataset(client: httpx.AsyncClient) -> None:
    response = await client.post(
        "/datasets/",
        json={
            "title": "Example",
            "description": "Some example items",
        },
    )
    assert response.status_code == 201
    data = response.json()
    pk = data["id"]
    assert isinstance(pk, int)
    assert data == {
        "id": pk,
        "title": "Example",
        "description": "Some example items",
    }

    response = await client.get("/datasets/4242/")
    assert response.status_code == 404

    response = await client.get(f"/datasets/{pk}/")
    assert response.status_code == 200
    assert response.json() == data

    response = await client.get("/datasets/")
    assert response.status_code == 200
    assert response.json() == [data]

    response = await client.delete(f"/datasets/{pk}/")
    assert response.status_code == 204

    response = await client.get(f"/datasets/{pk}/")
    assert response.status_code == 404

    response = await client.get("/datasets/")
    assert response.status_code == 200
    assert response.json() == []
