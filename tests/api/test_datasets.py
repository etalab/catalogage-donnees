import httpx
import pytest

from server.application.datasets.commands import CreateDataset
from server.application.datasets.queries import GetDatasetByID
from server.config.di import resolve
from server.domain.common.types import id_factory
from server.domain.datasets.entities import DataFormat
from server.domain.datasets.exceptions import DatasetDoesNotExist
from server.seedwork.application.messages import MessageBus


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "payload, expected_errors_attrs",
    [
        pytest.param(
            {},
            [
                {"loc": ["body", "title"], "type": "value_error.missing"},
                {"loc": ["body", "description"], "type": "value_error.missing"},
                {"loc": ["body", "formats"], "type": "value_error.missing"},
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
async def test_dataset_crud(client: httpx.AsyncClient) -> None:
    response = await client.post(
        "/datasets/",
        json={
            "title": "Example",
            "description": "Some example items",
            "formats": ["website"],
        },
    )
    assert response.status_code == 201
    data = response.json()
    pk = data["id"]
    assert isinstance(pk, str)
    assert data == {
        "id": pk,
        "title": "Example",
        "description": "Some example items",
        "formats": ["website"],
    }

    non_existing_id = id_factory()
    response = await client.get(f"/datasets/{non_existing_id}/")
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


CREATE_EXAMPLE_DATASET = CreateDataset(
    title="Example title",
    description="Example description",
    formats=["website", "api"],
)


@pytest.mark.asyncio
class TestDatasetUpdate:
    async def test_not_found(self, client: httpx.AsyncClient) -> None:
        response = await client.put(
            f"/datasets/{id_factory()}/",
            json={
                "title": "Title",
                "description": "Description",
                "formats": ["website"],
            },
        )
        assert response.status_code == 404

    async def test_full_entity_expected(self, client: httpx.AsyncClient) -> None:
        bus = resolve(MessageBus)
        dataset_id = await bus.execute(CREATE_EXAMPLE_DATASET)

        # Apply PUT semantics, which expect a full entity.
        response = await client.put(f"/datasets/{dataset_id}/", json={})
        assert response.status_code == 422
        err_title, err_description, err_formats = response.json()["detail"]
        assert err_title["loc"] == ["body", "title"]
        assert err_title["type"] == "value_error.missing"
        assert err_description["loc"] == ["body", "description"]
        assert err_description["type"] == "value_error.missing"
        assert err_formats["loc"] == ["body", "formats"]
        assert err_formats["type"] == "value_error.missing"

    async def test_fields_empty_invalid(self, client: httpx.AsyncClient) -> None:
        bus = resolve(MessageBus)
        dataset_id = await bus.execute(CREATE_EXAMPLE_DATASET)

        response = await client.put(
            f"/datasets/{dataset_id}/",
            json={"title": "", "description": "", "formats": []},
        )
        assert response.status_code == 422

        err_title, err_description, err_formats = response.json()["detail"]

        assert err_title["loc"] == ["body", "title"]
        assert "empty" in err_title["msg"]

        assert err_description["loc"] == ["body", "description"]
        assert "empty" in err_description["msg"]

        assert err_formats["loc"] == ["body", "formats"]
        assert "at least one" in err_formats["msg"].lower()

    async def test_update(self, client: httpx.AsyncClient) -> None:
        bus = resolve(MessageBus)
        dataset_id = await bus.execute(CREATE_EXAMPLE_DATASET)

        response = await client.put(
            f"/datasets/{dataset_id}/",
            json={
                "title": "Other title",
                "description": "Other description",
                "formats": ["database"],
            },
        )
        assert response.status_code == 200

        # API returns updated representation
        assert response.json() == {
            "id": str(dataset_id),
            "title": "Other title",
            "description": "Other description",
            "formats": ["database"],
        }

        # Entity was indeed updated
        query = GetDatasetByID(id=dataset_id)
        dataset = await bus.execute(query)
        assert dataset.title == "Other title"
        assert dataset.description == "Other description"
        assert dataset.formats == [DataFormat.DATABASE]


@pytest.mark.asyncio
class TestFormats:
    async def test_formats_add(self, client: httpx.AsyncClient) -> None:
        bus = resolve(MessageBus)
        dataset_id = await bus.execute(CREATE_EXAMPLE_DATASET)

        response = await client.put(
            f"/datasets/{dataset_id}/",
            json={
                **CREATE_EXAMPLE_DATASET.dict(exclude={"formats"}),
                "formats": ["website", "api", "file_gis"],
            },
        )

        assert response.status_code == 200
        assert sorted(response.json()["formats"]) == ["api", "file_gis", "website"]

    async def test_formats_remove(self, client: httpx.AsyncClient) -> None:
        bus = resolve(MessageBus)
        dataset_id = await bus.execute(CREATE_EXAMPLE_DATASET)

        response = await client.put(
            f"/datasets/{dataset_id}/",
            json={
                **CREATE_EXAMPLE_DATASET.dict(exclude={"formats"}),
                "formats": ["website"],
            },
        )

        assert response.status_code == 200
        assert response.json()["formats"] == ["website"]


@pytest.mark.asyncio
class TestDeleteDataset:
    async def test_delete(self, client: httpx.AsyncClient) -> None:
        bus = resolve(MessageBus)

        command = CREATE_EXAMPLE_DATASET
        dataset_id = await bus.execute(command)

        response = await client.delete(f"/datasets/{dataset_id}/")
        assert response.status_code == 204

        query = GetDatasetByID(id=dataset_id)
        with pytest.raises(DatasetDoesNotExist):
            await bus.execute(query)

    async def test_idempotent(self, client: httpx.AsyncClient) -> None:
        # Repeated calls on a deleted (or non-existing) resource should be fine.
        dataset_id = id_factory()
        response = await client.delete(f"/datasets/{dataset_id}/")
        assert response.status_code == 204
