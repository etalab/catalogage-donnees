import httpx
import pytest

from server.application.auth.commands import CreateUser
from server.application.auth.queries import GetUserByEmail
from server.config.di import resolve
from server.domain.auth.entities import User
from server.domain.auth.exceptions import UserDoesNotExist
from server.seedwork.application.messages import MessageBus

from ..utils import authenticate


@pytest.mark.asyncio
async def test_create_user_user_role_denied(client: httpx.AsyncClient) -> None:
    payload = {"email": "john@doe.com"}
    request = client.build_request("POST", "/auth/users/", json=payload)
    response = await client.send(request)
    assert response.status_code == 403


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "payload, expected_error_attrs",
    [
        pytest.param(
            {},
            {"loc": ["body", "email"], "type": "value_error.missing"},
            id="empty",
        ),
        pytest.param(
            {"email": "john"},
            {"type": "value_error.email"},
            id="invalid-email-no-domain",
        ),
        pytest.param(
            {"email": "john@doe"},
            {"type": "value_error.email"},
            id="invalid-email-no-domain-extension",
        ),
        pytest.param(
            {"email": "johndoe.com"},
            {"type": "value_error.email"},
            id="invalid-email-no-@",
        ),
        pytest.param(
            {"email": "john@"},
            {"type": "value_error.email"},
            id="invalid-email-no-suffix",
        ),
        pytest.param(
            {"email": "@doe.com"},
            {"type": "value_error.email"},
            id="invalid-email-no-prefix",
        ),
    ],
)
async def test_create_user_invalid(
    client: httpx.AsyncClient,
    admin_user: User,
    payload: dict,
    expected_error_attrs: dict,
) -> None:
    request = client.build_request("POST", "/auth/users/", json=payload)
    authenticate(request, admin_user)

    response = await client.send(request)
    assert response.status_code == 422

    data = response.json()
    assert len(data["detail"]) == 1

    error_attrs = {key: data["detail"][0][key] for key in expected_error_attrs}
    assert error_attrs == expected_error_attrs


@pytest.mark.asyncio
async def test_create_user(client: httpx.AsyncClient, admin_user: User) -> None:
    payload = {"email": "john@doe.com"}
    request = client.build_request("POST", "/auth/users/", json=payload)
    authenticate(request, admin_user)

    response = await client.send(request)
    assert response.status_code == 201
    data = response.json()

    pk = data["id"]
    assert isinstance(pk, int)
    assert data == {"id": pk, "email": "john@doe.com", "role": "USER"}


@pytest.mark.asyncio
async def test_create_user_already_exists(
    client: httpx.AsyncClient, admin_user: User
) -> None:
    payload = {"email": "john@doe.com"}
    request = client.build_request("POST", "/auth/users/", json=payload)
    authenticate(request, admin_user)

    response = await client.send(request)
    assert response.status_code == 400


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "headers, status_code",
    [
        pytest.param(
            {},
            403,
            id="empty",
        ),
        pytest.param(
            {"X-Email": "gibberish"},
            403,
            id="invalid-email",
        ),
        pytest.param(
            {"X-Email": "doesnotexist@example.com"},
            403,
            id="user-does-not-exist",
        ),
        pytest.param(
            {"X-Email-Other": "john@doe.com"},
            403,
            id="wrong-scheme",
        ),
        pytest.param(
            {"X-Email": "john@doe.com"},
            200,
            id="valid",
        ),
        pytest.param(
            {"x-email": "john@doe.com"},
            200,
            id="valid-case-insensitive",
        ),
    ],
)
async def test_check_auth(
    client: httpx.AsyncClient, headers: dict, status_code: int
) -> None:
    response = await client.get("/auth/check/", headers=headers)

    assert response.status_code == status_code

    if status_code == 200:
        assert response.json() == {"is_authenticated": True}


@pytest.mark.asyncio
async def test_delete_user(client: httpx.AsyncClient, admin_user: User) -> None:
    bus = resolve(MessageBus)
    email = "temp@example.org"

    command = CreateUser(email=email)
    user_id = await bus.execute(command)

    request = client.build_request("DELETE", f"/auth/users/{user_id}/")
    authenticate(request, admin_user)
    response = await client.send(request)
    assert response.status_code == 204

    query = GetUserByEmail(email=email)
    with pytest.raises(UserDoesNotExist):
        await bus.execute(query)


@pytest.mark.asyncio
async def test_delete_user_idempotent(
    client: httpx.AsyncClient, admin_user: User
) -> None:
    # Represents a non-existing user, or a user previously deleted.
    # These should be handled the same way as existing users by
    # this endpoint (idempotency).
    user_id = 4242

    request = client.build_request("DELETE", f"/auth/users/{user_id}/")
    authenticate(request, admin_user)
    response = await client.send(request)
    assert response.status_code == 204
