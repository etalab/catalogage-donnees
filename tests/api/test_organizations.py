import httpx
import pytest

from ..factories import CreateOrganizationFactory
from ..helpers import TestUser, to_payload


def api_key_auth(request: httpx.Request) -> httpx.Request:
    request.headers["X-Api-Key"] = "<testing>"
    return request


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "payload, expected_errors_attrs",
    [
        pytest.param(
            {},
            [
                {"loc": ["body", "name"], "type": "value_error.missing"},
                {"loc": ["body", "siret"], "type": "value_error.missing"},
            ],
            id="missing-fields",
        ),
        pytest.param(
            {
                "name": "Example organization",
                "siret": "invalidsiret",
            },
            [
                {
                    "loc": ["body", "siret"],
                    "msg": "must contain digits only",
                }
            ],
            id="siret-invalid",
        ),
    ],
)
async def test_create_organization_invalid(
    client: httpx.AsyncClient,
    temp_user: TestUser,
    payload: dict,
    expected_errors_attrs: list,
) -> None:
    response = await client.post("/organizations/", json=payload, auth=api_key_auth)
    assert response.status_code == 422

    data = response.json()
    assert len(data["detail"]) == len(expected_errors_attrs), data["detail"]

    for error, expected_error_attrs in zip(data["detail"], expected_errors_attrs):
        error_attrs = {key: error[key] for key in expected_error_attrs}
        assert error_attrs == expected_error_attrs


@pytest.mark.asyncio
async def test_create_organization(client: httpx.AsyncClient) -> None:
    siret = "604 876 475 00499"

    payload = to_payload(
        CreateOrganizationFactory.build(siret=siret, name="Example organization")
    )

    response = await client.post("/organizations/", json=payload, auth=api_key_auth)
    assert response.status_code == 201
    assert response.json() == {
        "siret": "60487647500499",
        "name": "Example organization",
    }


@pytest.mark.asyncio
async def test_create_organization_many(client: httpx.AsyncClient) -> None:
    for _ in range(5):
        command = CreateOrganizationFactory.build()
        payload = to_payload(command)
        response = await client.post("/organizations/", json=payload, auth=api_key_auth)
        assert response.status_code == 201
        assert response.json() == {"siret": command.siret, "name": command.name}


@pytest.mark.asyncio
async def test_create_organization_already_exists(client: httpx.AsyncClient) -> None:
    command = CreateOrganizationFactory.build()
    payload = to_payload(command)
    response = await client.post("/organizations/", json=payload, auth=api_key_auth)
    assert response.status_code == 201
    org = response.json()

    payload = to_payload(CreateOrganizationFactory.build(siret=command.siret))
    response = await client.post("/organizations/", json=payload, auth=api_key_auth)
    assert response.status_code == 200
    assert response.json() == org


@pytest.mark.asyncio
class TestOrganizationPermissions:
    async def test_create_anonymous(self, client: httpx.AsyncClient) -> None:
        response = await client.post(
            "/organizations/",
            json=to_payload(CreateOrganizationFactory.build()),
        )
        assert response.status_code == 403

    async def test_create_authenticated(
        self, client: httpx.AsyncClient, temp_user: TestUser
    ) -> None:
        response = await client.post(
            "/organizations/",
            json=to_payload(CreateOrganizationFactory.build()),
            auth=temp_user.auth,
        )
        assert response.status_code == 403
