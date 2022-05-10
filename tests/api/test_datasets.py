import datetime as dt
from typing import Any, List

import httpx
import pytest

from server.application.datasets.commands import CreateDataset
from server.application.datasets.queries import GetDatasetByID
from server.application.tags.commands import CreateTag
from server.application.tags.queries import GetTagByID
from server.config.di import resolve
from server.domain.catalog_records.repositories import CatalogRecordRepository
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
                {"loc": ["body", "contact_emails"], "type": "value_error.missing"},
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
                "contact_emails": ["person@mydomain.org"],
            },
            [
                {
                    "loc": ["body", "formats"],
                    "msg": "formats must contain at least one item",
                }
            ],
            id="formats-empty",
        ),
        pytest.param(
            {
                "title": "Title",
                "description": "Description",
                "service": "Service",
                "geographical_coverage": "national",
                "formats": ["api"],
                "contact_emails": [],
            },
            [
                {
                    "loc": ["body", "contact_emails"],
                    "msg": "contact_emails must contain at least one item",
                }
            ],
            id="contact_emails-empty",
        ),
    ],
)
async def test_create_dataset_invalid(
    client: httpx.AsyncClient,
    temp_user: TestUser,
    payload: dict,
    expected_errors_attrs: list,
) -> None:
    response = await client.post("/datasets/", json=payload, auth=temp_user.auth)
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
    "producer_email": "example.service@mydomain.org",
    "contact_emails": ["example.person@mydomain.org"],
    "update_frequency": "weekly",
    "last_updated_at": known_date.isoformat(),
    "published_url": None,
    "tag_ids": [],
}

CREATE_ANY_DATASET = CreateDataset(
    title="Title",
    description="Description",
    service="Example service",
    geographical_coverage=GeographicalCoverage.NATIONAL,
    formats=[DataFormat.WEBSITE, DataFormat.API],
    contact_emails=["person@mydomain.org"],
)


@pytest.mark.asyncio
async def test_dataset_crud(
    client: httpx.AsyncClient, temp_user: TestUser, admin_user: TestUser
) -> None:
    response = await client.post(
        "/datasets/", json=CREATE_DATASET_PAYLOAD, auth=temp_user.auth
    )
    assert response.status_code == 201
    data = response.json()

    pk = data["id"]
    assert isinstance(pk, str)

    created_at = data["catalog_record"]["created_at"]
    assert dtutil.parse(created_at) == approx_datetime(
        dtutil.now(), abs=dt.timedelta(seconds=0.2)
    )

    assert data == {
        "id": pk,
        "catalog_record": {
            "id": data["catalog_record"]["id"],
            "created_at": created_at,
        },
        "title": "Example title",
        "description": "Example description",
        "service": "Example service",
        "geographical_coverage": "national",
        "formats": ["website"],
        "technical_source": "Example database",
        "producer_email": "example.service@mydomain.org",
        "contact_emails": ["example.person@mydomain.org"],
        "update_frequency": "weekly",
        "last_updated_at": known_date.isoformat(),
        "published_url": None,
        "tags": [],
    }

    non_existing_id = id_factory()

    response = await client.get(f"/datasets/{non_existing_id}/", auth=temp_user.auth)
    assert response.status_code == 404

    response = await client.get(f"/datasets/{pk}/", auth=temp_user.auth)
    assert response.status_code == 200
    assert response.json() == data

    response = await client.get("/datasets/", auth=temp_user.auth)
    assert response.status_code == 200
    assert response.json()["items"] == [data]

    response = await client.delete(f"/datasets/{pk}/", auth=admin_user.auth)
    assert response.status_code == 204

    response = await client.get(f"/datasets/{pk}/", auth=temp_user.auth)
    assert response.status_code == 404

    response = await client.get("/datasets/", auth=temp_user.auth)
    assert response.status_code == 200
    assert response.json()["items"] == []


@pytest.mark.asyncio
class TestDatasetPermissions:
    async def test_create_not_authenticated(self, client: httpx.AsyncClient) -> None:
        response = await client.post("/datasets/", json=CREATE_DATASET_PAYLOAD)
        assert response.status_code == 401

    async def test_get_not_authenticated(self, client: httpx.AsyncClient) -> None:
        pk = id_factory()
        response = await client.get(f"/datasets/{pk}/")
        assert response.status_code == 401

    async def test_list_not_authenticated(self, client: httpx.AsyncClient) -> None:
        response = await client.get("/datasets/")
        assert response.status_code == 401

    async def test_update_not_authenticated(self, client: httpx.AsyncClient) -> None:
        pk = id_factory()
        response = await client.put(f"/datasets/{pk}/", json={})
        assert response.status_code == 401

    async def test_delete_not_authenticated(self, client: httpx.AsyncClient) -> None:
        pk = id_factory()
        response = await client.delete(f"/datasets/{pk}/")
        assert response.status_code == 401

    async def test_delete_not_admin(
        self, client: httpx.AsyncClient, temp_user: TestUser
    ) -> None:
        pk = id_factory()
        response = await client.delete(f"/datasets/{pk}/", auth=temp_user.auth)
        assert response.status_code == 403


async def add_dataset_pagination_corpus(n: int) -> None:
    bus = resolve(MessageBus)

    for k in range(1, n + 1):
        await bus.execute(CREATE_ANY_DATASET.copy(update={"title": f"Dataset {k}"}))


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "params, num_items, dataset_titles",
    [
        pytest.param(
            {},
            13,
            ["__skip__"],
            id="default",
        ),
        pytest.param(
            {"page_size": 3},
            3,
            ["Dataset 13", "Dataset 12", "Dataset 11"],
            id="first-page",
        ),
        pytest.param(
            {"page_size": 3, "page_number": 4},
            3,
            ["Dataset 4", "Dataset 3", "Dataset 2"],
            id="some-middle-page",
        ),
        pytest.param(
            {"page_size": 3, "page_number": 5},
            1,
            ["Dataset 1"],
            id="last-page",
        ),
        pytest.param(
            {"page_size": 3, "page_number": 6},
            0,
            [],
            id="beyond-last-page",
        ),
    ],
)
async def test_dataset_pagination(
    client: httpx.AsyncClient,
    temp_user: TestUser,
    params: dict,
    num_items: int,
    dataset_titles: List[str],
) -> None:
    await add_dataset_pagination_corpus(n=13)

    response = await client.get("/datasets/", params=params, auth=temp_user.auth)
    assert response.status_code == 200
    data = response.json()

    assert len(data["items"]) == num_items
    assert data["total_items"] == 13
    assert data["page_size"] == params.get("page_size", 1000)
    if "__skip__" not in dataset_titles:
        assert [item["title"] for item in data["items"]] == dataset_titles


@pytest.mark.asyncio
async def test_dataset_get_all_uses_reverse_chronological_order(
    client: httpx.AsyncClient, temp_user: TestUser
) -> None:
    bus = resolve(MessageBus)
    await bus.execute(CREATE_ANY_DATASET.copy(update={"title": "Oldest"}))
    await bus.execute(CREATE_ANY_DATASET.copy(update={"title": "Intermediate"}))
    await bus.execute(CREATE_ANY_DATASET.copy(update={"title": "Newest"}))

    response = await client.get("/datasets/", auth=temp_user.auth)
    assert response.status_code == 200
    titles = [dataset["title"] for dataset in response.json()["items"]]
    assert titles == ["Newest", "Intermediate", "Oldest"]


@pytest.mark.asyncio
class TestDatasetOptionalFields:
    @pytest.mark.parametrize(
        "field, default",
        [
            pytest.param("technical_source", None),
            pytest.param("producer_email", None),
            pytest.param("update_frequency", None),
            pytest.param("last_updated_at", None),
        ],
    )
    async def test_optional_fields_missing_uses_defaults(
        self, client: httpx.AsyncClient, temp_user: TestUser, field: str, default: Any
    ) -> None:
        payload = CREATE_DATASET_PAYLOAD.copy()
        payload.pop(field)
        response = await client.post("/datasets/", json=payload, auth=temp_user.auth)
        assert response.status_code == 201
        dataset = response.json()
        assert dataset[field] == default

    async def test_optional_fields_invalid(
        self, client: httpx.AsyncClient, temp_user: TestUser
    ) -> None:
        response = await client.post(
            "/datasets/",
            json={
                **CREATE_DATASET_PAYLOAD,
                "geographical_coverage": "not_in_enum",
                "contact_emails": ["notanemail", "valid@mydomain.org"],
                "update_frequency": "not_in_enum",
                "last_updated_at": "not_a_datetime",
            },
            auth=temp_user.auth,
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
    async def test_not_found(
        self, client: httpx.AsyncClient, temp_user: TestUser
    ) -> None:
        response = await client.put(
            f"/datasets/{id_factory()}/",
            json=CREATE_DATASET_PAYLOAD,
            auth=temp_user.auth,
        )
        assert response.status_code == 404

    async def test_full_entity_expected(
        self, client: httpx.AsyncClient, temp_user: TestUser
    ) -> None:
        bus = resolve(MessageBus)
        dataset_id = await bus.execute(CREATE_ANY_DATASET)

        # Apply PUT semantics, which expect a full entity.
        response = await client.put(
            f"/datasets/{dataset_id}/", json={}, auth=temp_user.auth
        )
        assert response.status_code == 422
        fields = [
            "title",
            "description",
            "service",
            "geographical_coverage",
            "formats",
            "technical_source",
            "producer_email",
            "contact_emails",
            "update_frequency",
            "last_updated_at",
            "published_url",
            "tag_ids",
        ]
        errors = response.json()["detail"]
        assert len(errors) == len(fields)
        for field, error in zip(fields, errors):
            assert error["loc"] == ["body", field], field
            assert error["type"] == "value_error.missing", field

    async def test_fields_empty_invalid(
        self, client: httpx.AsyncClient, temp_user: TestUser
    ) -> None:
        bus = resolve(MessageBus)
        dataset_id = await bus.execute(CREATE_ANY_DATASET)

        response = await client.put(
            f"/datasets/{dataset_id}/",
            json={
                "title": "",
                "description": "",
                "service": "",
                "formats": ["website", "api"],
                "geographical_coverage": "national",
                "producer_email": None,
                "technical_source": "",
                "contact_emails": ["person@mydomain.org"],
                "update_frequency": "weekly",
                "last_updated_at": known_date.isoformat(),
                "published_url": "",
                "tag_ids": [],
            },
            auth=temp_user.auth,
        )
        assert response.status_code == 422

        (
            err_title,
            err_description,
            err_service,
            err_published_url,
        ) = response.json()["detail"]

        assert err_title["loc"] == ["body", "title"]
        assert "empty" in err_title["msg"]

        assert err_description["loc"] == ["body", "description"]
        assert "empty" in err_description["msg"]

        assert err_service["loc"] == ["body", "service"]
        assert "empty" in err_service["msg"]

        assert err_published_url["loc"] == ["body", "published_url"]
        assert "empty" in err_service["msg"]

    async def test_update(self, client: httpx.AsyncClient, temp_user: TestUser) -> None:
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
                "producer_email": "other.service@mydomain.org",
                "contact_emails": ["other.person@mydomain.org"],
                "update_frequency": "weekly",
                "last_updated_at": other_known_date.isoformat(),
                "published_url": "https://data.gouv.fr/datasets/other",
                "tag_ids": [],
            },
            auth=temp_user.auth,
        )
        assert response.status_code == 200

        # API returns updated representation
        data = response.json()
        assert data == {
            "id": str(dataset_id),
            "catalog_record": data["catalog_record"],
            "title": "Other title",
            "description": "Other description",
            "service": "Other service",
            "geographical_coverage": "region",
            "formats": ["database"],
            "technical_source": "Other information system",
            "producer_email": "other.service@mydomain.org",
            "contact_emails": ["other.person@mydomain.org"],
            "update_frequency": "weekly",
            "last_updated_at": other_known_date.isoformat(),
            "published_url": "https://data.gouv.fr/datasets/other",
            "tags": [],
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
        assert dataset.producer_email == "other.service@mydomain.org"
        assert dataset.contact_emails == ["other.person@mydomain.org"]
        assert dataset.update_frequency == UpdateFrequency.WEEKLY
        assert dataset.last_updated_at == other_known_date
        assert dataset.published_url == "https://data.gouv.fr/datasets/other"


@pytest.mark.asyncio
class TestFormats:
    async def test_formats_add(
        self, client: httpx.AsyncClient, temp_user: TestUser
    ) -> None:
        bus = resolve(MessageBus)
        dataset_id = await bus.execute(CREATE_ANY_DATASET)

        response = await client.put(
            f"/datasets/{dataset_id}/",
            json={
                **CREATE_ANY_DATASET.dict(),
                "geographical_coverage": CREATE_ANY_DATASET.geographical_coverage.value,
                "formats": ["website", "api", "file_gis"],
            },
            auth=temp_user.auth,
        )

        assert response.status_code == 200
        assert sorted(response.json()["formats"]) == ["api", "file_gis", "website"]

    async def test_formats_remove(
        self, client: httpx.AsyncClient, temp_user: TestUser
    ) -> None:
        bus = resolve(MessageBus)
        dataset_id = await bus.execute(CREATE_ANY_DATASET)

        response = await client.put(
            f"/datasets/{dataset_id}/",
            json={
                **CREATE_ANY_DATASET.dict(),
                "geographical_coverage": CREATE_ANY_DATASET.geographical_coverage.value,
                "formats": ["website"],
            },
            auth=temp_user.auth,
        )

        assert response.status_code == 200
        assert response.json()["formats"] == ["website"]


@pytest.mark.asyncio
class TestTags:
    async def test_tags_add(
        self, client: httpx.AsyncClient, temp_user: TestUser
    ) -> None:
        bus = resolve(MessageBus)

        dataset_id = await bus.execute(CREATE_ANY_DATASET)
        tag_architecture_id = await bus.execute(CreateTag(name="Architecture"))
        tag_architecture = await bus.execute(GetTagByID(id=tag_architecture_id))

        response = await client.put(
            f"/datasets/{dataset_id}/",
            json={
                **CREATE_ANY_DATASET.dict(),
                "geographical_coverage": CREATE_ANY_DATASET.geographical_coverage.value,
                "formats": [fmt.value for fmt in CREATE_ANY_DATASET.formats],
                "tag_ids": [str(tag_architecture.id)],
            },
            auth=temp_user.auth,
        )
        assert response.status_code == 200
        assert response.json()["tags"] == [
            {"id": str(tag_architecture.id), "name": "Architecture"},
        ]

        dataset = await bus.execute(GetDatasetByID(id=dataset_id))
        assert dataset.tags == [tag_architecture]

    async def test_tags_remove(
        self, client: httpx.AsyncClient, temp_user: TestUser
    ) -> None:
        bus = resolve(MessageBus)

        tag_architecture_id = await bus.execute(CreateTag(name="Architecture"))
        tag_architecture = await bus.execute(GetTagByID(id=tag_architecture_id))
        dataset_id = await bus.execute(
            CREATE_ANY_DATASET.copy(update={"tag_ids": [str(tag_architecture.id)]})
        )

        response = await client.put(
            f"/datasets/{dataset_id}/",
            json={
                **CREATE_ANY_DATASET.dict(),
                "geographical_coverage": CREATE_ANY_DATASET.geographical_coverage.value,
                "formats": [fmt.value for fmt in CREATE_ANY_DATASET.formats],
                "tag_ids": [],
            },
            auth=temp_user.auth,
        )
        assert response.status_code == 200
        assert response.json()["tags"] == []

        dataset = await bus.execute(GetDatasetByID(id=dataset_id))
        assert dataset.tags == []


@pytest.mark.asyncio
class TestDeleteDataset:
    async def test_delete(
        self, client: httpx.AsyncClient, admin_user: TestUser
    ) -> None:
        bus = resolve(MessageBus)

        dataset_id = await bus.execute(CREATE_ANY_DATASET)
        dataset = await bus.execute(GetDatasetByID(id=dataset_id))

        response = await client.delete(f"/datasets/{dataset_id}/", auth=admin_user.auth)
        assert response.status_code == 204

        query = GetDatasetByID(id=dataset_id)
        with pytest.raises(DatasetDoesNotExist):
            await bus.execute(query)

        # Verify cascades
        catalog_record_repository = resolve(CatalogRecordRepository)
        assert (
            await catalog_record_repository.get_by_id(dataset.catalog_record.id) is None
        )

    async def test_idempotent(
        self, client: httpx.AsyncClient, admin_user: TestUser
    ) -> None:
        # Repeated calls on a deleted (or non-existing) resource should be fine.
        dataset_id = id_factory()
        response = await client.delete(f"/datasets/{dataset_id}/", auth=admin_user.auth)
        assert response.status_code == 204
