import datetime as dt
from typing import Any

import httpx
import pytest

from server.application.datasets.commands import CreateDataset
from server.application.datasets.queries import GetDatasetByID
from server.config.di import resolve
from server.domain.common import datetime as dtutil
from server.domain.common.types import id_factory
from server.domain.datasets.entities import (
    DataFormat,
    GeographicalCoverage,
    UpdateFrequency,
)
from server.domain.datasets.exceptions import DatasetDoesNotExist
from server.seedwork.application.messages import MessageBus

from ..helpers import TestUser, approx_datetime


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "payload, expected_errors_attrs",
    [
        pytest.param(
            {},
            [
                {"loc": ["body", "title"], "type": "value_error.missing"},
                {"loc": ["body", "description"], "type": "value_error.missing"},
                {"loc": ["body", "service"], "type": "value_error.missing"},
                {
                    "loc": ["body", "geographical_coverage"],
                    "type": "value_error.missing",
                },
                {"loc": ["body", "formats"], "type": "value_error.missing"},
                {"loc": ["body", "entrypoint_email"], "type": "value_error.missing"},
            ],
            id="missing-fields",
        ),
        pytest.param(
            {
                "title": "Title",
                "description": "Description",
                "service": "Service",
                "geographical_coverage": "national",
                "formats": [],
                "entrypoint_email": "service@mydomain.org",
            },
            [
                {
                    "loc": ["body", "formats"],
                    "msg": "formats must contain at least one item",
                }
            ],
            id="formats-empty",
        ),
    ],
)
async def test_create_dataset_invalid(
    client: httpx.AsyncClient, payload: dict, expected_errors_attrs: list
) -> None:
    response = await client.post("/datasets/", json=payload)
    assert response.status_code == 422

    data = response.json()
    assert len(data["detail"]) == len(expected_errors_attrs), data["detail"]

    for error, expected_error_attrs in zip(data["detail"], expected_errors_attrs):
        error_attrs = {key: error[key] for key in expected_error_attrs}
        assert error_attrs == expected_error_attrs


known_date = dtutil.parse("2022-01-04T10:15:19.121212+00:00")

CREATE_DATASET_PAYLOAD = {
    "title": "Example title",
    "description": "Example description",
    "service": "Example service",
    "geographical_coverage": "national",
    "formats": ["website"],
    "technical_source": "Example database",
    "entrypoint_email": "example.service@mydomain.org",
    "contact_emails": ["example.person@mydomain.org"],
    "update_frequency": "weekly",
    "last_updated_at": known_date.isoformat(),
}

CREATE_ANY_DATASET = CreateDataset(
    title="Title",
    description="Description",
    service="Example service",
    geographical_coverage=GeographicalCoverage.NATIONAL,
    formats=[DataFormat.WEBSITE, DataFormat.API],
    entrypoint_email="service@mydomain.org",
)


@pytest.mark.asyncio
async def test_dataset_crud(client: httpx.AsyncClient, admin_user: TestUser) -> None:
    response = await client.post("/datasets/", json=CREATE_DATASET_PAYLOAD)
    assert response.status_code == 201
    data = response.json()

    pk = data["id"]
    assert isinstance(pk, str)

    created_at = data["created_at"]
    assert dtutil.parse(created_at) == approx_datetime(
        dtutil.now(), abs=dt.timedelta(seconds=0.1)
    )

    assert data == {
        "id": pk,
        "created_at": created_at,
        "title": "Example title",
        "description": "Example description",
        "service": "Example service",
        "geographical_coverage": "national",
        "formats": ["website"],
        "technical_source": "Example database",
        "entrypoint_email": "example.service@mydomain.org",
        "contact_emails": ["example.person@mydomain.org"],
        "update_frequency": "weekly",
        "last_updated_at": known_date.isoformat(),
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

    response = await client.delete(f"/datasets/{pk}/", auth=admin_user.auth)
    assert response.status_code == 204

    response = await client.get(f"/datasets/{pk}/")
    assert response.status_code == 404

    response = await client.get("/datasets/")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_dataset_get_all_uses_reverse_chronological_order(
    client: httpx.AsyncClient,
) -> None:
    bus = resolve(MessageBus)
    await bus.execute(CREATE_ANY_DATASET.copy(update={"title": "Oldest"}))
    await bus.execute(CREATE_ANY_DATASET.copy(update={"title": "Intermediate"}))
    await bus.execute(CREATE_ANY_DATASET.copy(update={"title": "Newest"}))

    response = await client.get("/datasets/")
    assert response.status_code == 200
    titles = [dataset["title"] for dataset in response.json()]
    assert titles == ["Newest", "Intermediate", "Oldest"]


@pytest.mark.asyncio
class TestDatasetOptionalFields:
    @pytest.mark.parametrize(
        "field, default",
        [
            pytest.param("technical_source", None),
            pytest.param("contact_emails", []),
            pytest.param("update_frequency", None),
            pytest.param("last_updated_at", None),
        ],
    )
    async def test_optional_fields_missing_uses_defaults(
        self, client: httpx.AsyncClient, field: str, default: Any
    ) -> None:
        payload = CREATE_DATASET_PAYLOAD.copy()
        payload.pop(field)
        response = await client.post("/datasets/", json=payload)
        assert response.status_code == 201
        dataset = response.json()
        assert dataset[field] == default

    async def test_optional_fields_invalid(self, client: httpx.AsyncClient) -> None:
        response = await client.post(
            "/datasets/",
            json={
                **CREATE_DATASET_PAYLOAD,
                "geographical_coverage": "not_in_enum",
                "contact_emails": ["notanemail", "valid@mydomain.org"],
                "update_frequency": "not_in_enum",
                "last_updated_at": "not_a_datetime",
            },
        )
        assert response.status_code == 422
        (
            err_geographical_coverage,
            err_contact_emails,
            err_update_frequency,
            err_last_updated_at,
        ) = response.json()["detail"]
        assert err_geographical_coverage["loc"] == ["body", "geographical_coverage"]
        assert err_geographical_coverage["type"] == "type_error.enum"
        assert err_contact_emails["loc"] == ["body", "contact_emails", 0]
        assert err_contact_emails["type"] == "value_error.email"
        assert err_update_frequency["loc"] == ["body", "update_frequency"]
        assert err_update_frequency["type"] == "type_error.enum"
        assert err_last_updated_at["loc"] == ["body", "last_updated_at"]
        assert err_last_updated_at["type"] == "value_error.datetime"


@pytest.mark.asyncio
class TestDatasetUpdate:
    async def test_not_found(self, client: httpx.AsyncClient) -> None:
        response = await client.put(
            f"/datasets/{id_factory()}/",
            json=CREATE_DATASET_PAYLOAD,
        )
        assert response.status_code == 404

    async def test_full_entity_expected(self, client: httpx.AsyncClient) -> None:
        bus = resolve(MessageBus)
        dataset_id = await bus.execute(CREATE_ANY_DATASET)

        # Apply PUT semantics, which expect a full entity.
        response = await client.put(f"/datasets/{dataset_id}/", json={})
        assert response.status_code == 422
        fields = [
            "title",
            "description",
            "service",
            "geographical_coverage",
            "formats",
            "technical_source",
            "entrypoint_email",
            "contact_emails",
            "update_frequency",
            "last_updated_at",
        ]
        errors = response.json()["detail"]
        assert len(errors) == len(fields)
        for field, error in zip(fields, errors):
            assert error["loc"] == ["body", field], field
            assert error["type"] == "value_error.missing", field

    async def test_fields_empty_invalid(self, client: httpx.AsyncClient) -> None:
        bus = resolve(MessageBus)
        dataset_id = await bus.execute(CREATE_ANY_DATASET)

        response = await client.put(
            f"/datasets/{dataset_id}/",
            json={
                "title": "",
                "description": "",
                "service": "",
                "formats": [],
                "geographical_coverage": "national",
                "entrypoint_email": "service@mydomain.org",
                "technical_source": "",
                "contact_emails": [],
                "update_frequency": "weekly",
                "last_updated_at": known_date.isoformat(),
            },
        )
        assert response.status_code == 422

        err_title, err_description, err_service, err_formats = response.json()["detail"]

        assert err_title["loc"] == ["body", "title"]
        assert "empty" in err_title["msg"]

        assert err_description["loc"] == ["body", "description"]
        assert "empty" in err_description["msg"]

        assert err_service["loc"] == ["body", "service"]
        assert "empty" in err_service["msg"]

        assert err_formats["loc"] == ["body", "formats"]
        assert "at least one" in err_formats["msg"].lower()

    async def test_update(self, client: httpx.AsyncClient) -> None:
        bus = resolve(MessageBus)
        dataset_id = await bus.execute(CREATE_ANY_DATASET)

        other_known_date = dtutil.parse("2022-02-04T10:15:19.121212+00:00")

        response = await client.put(
            f"/datasets/{dataset_id}/",
            json={
                "title": "Other title",
                "description": "Other description",
                "service": "Other service",
                "geographical_coverage": "region",
                "formats": ["database"],
                "technical_source": "Other information system",
                "entrypoint_email": "other.service@mydomain.org",
                "contact_emails": ["other.person@mydomain.org"],
                "update_frequency": "weekly",
                "last_updated_at": other_known_date.isoformat(),
            },
        )
        assert response.status_code == 200

        # API returns updated representation
        data = response.json()
        assert data == {
            "id": str(dataset_id),
            "created_at": data["created_at"],
            "title": "Other title",
            "description": "Other description",
            "service": "Other service",
            "geographical_coverage": "region",
            "formats": ["database"],
            "technical_source": "Other information system",
            "entrypoint_email": "other.service@mydomain.org",
            "contact_emails": ["other.person@mydomain.org"],
            "update_frequency": "weekly",
            "last_updated_at": other_known_date.isoformat(),
        }

        # Entity was indeed updated
        query = GetDatasetByID(id=dataset_id)
        dataset = await bus.execute(query)
        assert dataset.title == "Other title"
        assert dataset.description == "Other description"
        assert dataset.service == "Other service"
        assert dataset.geographical_coverage == GeographicalCoverage.REGION
        assert dataset.formats == [DataFormat.DATABASE]
        assert dataset.technical_source == "Other information system"
        assert dataset.entrypoint_email == "other.service@mydomain.org"
        assert dataset.contact_emails == ["other.person@mydomain.org"]
        assert dataset.update_frequency == UpdateFrequency.WEEKLY
        assert dataset.last_updated_at == other_known_date


@pytest.mark.asyncio
class TestFormats:
    async def test_formats_add(self, client: httpx.AsyncClient) -> None:
        bus = resolve(MessageBus)
        dataset_id = await bus.execute(CREATE_ANY_DATASET)

        response = await client.put(
            f"/datasets/{dataset_id}/",
            json={
                **CREATE_ANY_DATASET.dict(),
                "geographical_coverage": CREATE_ANY_DATASET.geographical_coverage.value,
                "formats": ["website", "api", "file_gis"],
            },
        )

        assert response.status_code == 200
        assert sorted(response.json()["formats"]) == ["api", "file_gis", "website"]

    async def test_formats_remove(self, client: httpx.AsyncClient) -> None:
        bus = resolve(MessageBus)
        dataset_id = await bus.execute(CREATE_ANY_DATASET)

        response = await client.put(
            f"/datasets/{dataset_id}/",
            json={
                **CREATE_ANY_DATASET.dict(),
                "geographical_coverage": CREATE_ANY_DATASET.geographical_coverage.value,
                "formats": ["website"],
            },
        )

        assert response.status_code == 200
        assert response.json()["formats"] == ["website"]


@pytest.mark.asyncio
class TestDeleteDataset:
    async def test_delete(
        self, client: httpx.AsyncClient, temp_user: TestUser, admin_user: TestUser
    ) -> None:
        bus = resolve(MessageBus)

        dataset_id = await bus.execute(CREATE_ANY_DATASET)

        # Permissions
        response = await client.delete(f"/datasets/{dataset_id}/")
        assert response.status_code == 401
        response = await client.delete(f"/datasets/{dataset_id}/", auth=temp_user.auth)
        assert response.status_code == 403

        response = await client.delete(f"/datasets/{dataset_id}/", auth=admin_user.auth)
        assert response.status_code == 204

        query = GetDatasetByID(id=dataset_id)
        with pytest.raises(DatasetDoesNotExist):
            await bus.execute(query)

    async def test_idempotent(
        self, client: httpx.AsyncClient, admin_user: TestUser
    ) -> None:
        # Repeated calls on a deleted (or non-existing) resource should be fine.
        dataset_id = id_factory()
        response = await client.delete(f"/datasets/{dataset_id}/", auth=admin_user.auth)
        assert response.status_code == 204
