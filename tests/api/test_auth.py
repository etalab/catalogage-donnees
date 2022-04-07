from typing import List

import httpx
import pytest

from server.application.auth.queries import GetUserByEmail
from server.config.di import resolve
from server.domain.auth.exceptions import UserDoesNotExist
from server.domain.common.types import id_factory
from server.seedwork.application.messages import MessageBus

from ..helpers import TestUser


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "payload, expected_errors_attrs",
    [
        pytest.param(
            {},
            [
                {"loc": ["body", "email"], "type": "value_error.missing"},
                {"loc": ["body", "password"], "type": "value_error.missing"},
            ],
            id="empty",
        ),
        pytest.param(
            {"email": "john", "password": "s3kr3t"},
            [{"type": "value_error.email"}],
            id="invalid-email-no-domain",
        ),
        pytest.param(
            {"email": "john@doe", "password": "s3kr3t"},
            [{"type": "value_error.email"}],
            id="invalid-email-no-domain-extension",
        ),
        pytest.param(
            {"email": "johndoe.com", "password": "s3kr3t"},
            [{"type": "value_error.email"}],
            id="invalid-email-no-@",
        ),
        pytest.param(
            {"email": "john@", "password": "s3kr3t"},
            [{"type": "value_error.email"}],
            id="invalid-email-no-suffix",
        ),
        pytest.param(
            {"email": "@doe.com", "password": "s3kr3t"},
            [{"type": "value_error.email"}],
            id="invalid-email-no-prefix",
        ),
    ],
)
async def test_create_user_invalid(
    client: httpx.AsyncClient,
    admin_user: TestUser,
    payload: dict,
    expected_errors_attrs: List[dict],
) -> None:
    response = await client.post("/auth/users/", json=payload, auth=admin_user.auth)
    assert response.status_code == 422

    data = response.json()
    assert len(data["detail"]) == len(expected_errors_attrs)

    for error, expected_error_attrs in zip(data["detail"], expected_errors_attrs):
        error_attrs = {key: error[key] for key in expected_error_attrs}
        assert error_attrs == expected_error_attrs


@pytest.mark.asyncio
async def test_create_user(
    client: httpx.AsyncClient, temp_user: TestUser, admin_user: TestUser
) -> None:
    payload = {"email": "john@doe.com", "password": "s3kr3t"}

    # Permissions
    response = await client.post("/auth/users/", json=payload)
    assert response.status_code == 401
    response = await client.post("/auth/users/", json=payload, auth=temp_user.auth)
    assert response.status_code == 403

    response = await client.post("/auth/users/", json=payload, auth=admin_user.auth)
    assert response.status_code == 201
    user = response.json()
    pk = user.pop("id")
    assert isinstance(pk, str)
    assert user == {"email": "john@doe.com"}


@pytest.mark.asyncio
async def test_create_user_already_exists(
    client: httpx.AsyncClient, temp_user: TestUser, admin_user: TestUser
) -> None:
    payload = {"email": temp_user.email, "password": "somethingelse"}
    response = await client.post("/auth/users/", json=payload, auth=admin_user.auth)
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_login(client: httpx.AsyncClient, temp_user: TestUser) -> None:
    payload = {"email": temp_user.email, "password": temp_user.password}
    response = await client.post("/auth/login/", json=payload)
    assert response.status_code == 200
    user = response.json()
    assert user == {
        "id": str(temp_user.id),
        "email": temp_user.email,
        "api_token": temp_user.api_token,
    }


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "email, password",
    [
        pytest.param("bad@example.org", "{password}", id="bad-email"),
        pytest.param("{email}", "badpass", id="bad-password"),
    ],
)
async def test_login_failed(
    client: httpx.AsyncClient, email: str, password: str, temp_user: TestUser
) -> None:
    payload = {
        "email": email.format(email=temp_user.email),
        "password": password.format(password=temp_user.password),
    }
    response = await client.post("/auth/login/", json=payload)
    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == "Invalid credentials"


@pytest.mark.asyncio
async def test_check(client: httpx.AsyncClient, temp_user: TestUser) -> None:
    response = await client.get("/auth/check/", auth=temp_user.auth)
    assert response.status_code == 200


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "headers",
    [
        pytest.param({}, id="missing-header"),
        pytest.param({"Authorization": ""}, id="empty-header"),
        pytest.param({"Authorization": "{api_token}"}, id="missing-scheme"),
        pytest.param({"Authorization": "NotBearer {api_token}"}, id="bad-scheme"),
        pytest.param({"Authorization": "Bearer badtoken"}, id="bad-token"),
    ],
)
async def test_check_failed(
    client: httpx.AsyncClient, temp_user: TestUser, headers: dict
) -> None:
    if "Authorization" in headers:
        headers["Authorization"] = headers["Authorization"].format(
            api_token=temp_user.api_token
        )

    response = await client.get("/auth/check/", headers=headers)
    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == "Invalid credentials"


@pytest.mark.asyncio
async def test_delete_user(
    client: httpx.AsyncClient, temp_user: TestUser, admin_user: TestUser
) -> None:
    bus = resolve(MessageBus)

    # Permissions
    response = await client.delete(f"/auth/users/{temp_user.id}/")
    assert response.status_code == 401
    response = await client.delete(f"/auth/users/{temp_user.id}/", auth=temp_user.auth)
    assert response.status_code == 403

    response = await client.delete(f"/auth/users/{temp_user.id}/", auth=admin_user.auth)
    assert response.status_code == 204

    query = GetUserByEmail(email=temp_user.email)
    with pytest.raises(UserDoesNotExist):
        await bus.execute(query)


@pytest.mark.asyncio
async def test_delete_user_idempotent(
    client: httpx.AsyncClient, admin_user: TestUser
) -> None:
    # Represents a non-existing user, or a user previously deleted.
    # These should be handled the same way as existing users by
    # this endpoint (idempotency).
    user_id = id_factory()

    response = await client.delete(f"/auth/users/{user_id}/", auth=admin_user.auth)
    assert response.status_code == 204
