import httpx
import pytest
from sqlalchemy.ext.asyncio.session import AsyncSession

from server.apps.auth import User, queries


@pytest.fixture(scope="module", autouse=True)
async def setup(client: httpx.AsyncClient) -> None:
    response = await client.post(
        "/auth/users/",
        json={
            "email": "token@user.com",
            "full_name": "Token User",
            "password": "s3kr3t",
        },
    )
    assert response.status_code == 201


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "data, errors",
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
            {"email": "john@doe.com"},
            [
                {"loc": ["body", "password"], "type": "value_error.missing"},
            ],
            id="missing-password",
        ),
        pytest.param(
            {"password": "p@ssw0rd"},
            [
                {"loc": ["body", "email"], "type": "value_error.missing"},
            ],
            id="missing-email",
        ),
        pytest.param(
            {"email": "john", "password": "p@ssw0rd"},
            [
                {"type": "value_error.email"},
            ],
            id="invalid-email",
        ),
        pytest.param(
            {"email": "john@", "password": "p@ssw0rd"},
            [{"type": "value_error.email"}],
            id="invalid-email",
        ),
        pytest.param(
            {"email": "@doe.com", "password": "p@ssw0rd"},
            [
                {"type": "value_error.email"},
            ],
            id="invalid-email",
        ),
        pytest.param(
            {"email": "johndoe.com", "password": "p@ssw0rd"},
            [
                {"type": "value_error.email"},
            ],
            id="invalid-email",
        ),
    ],
)
async def test_create_user_invalid(
    client: httpx.AsyncClient, data: dict, errors: list
) -> None:
    response = await client.post("/auth/users/", json=data)
    assert response.status_code == 422

    data = response.json()
    assert len(data["detail"]) == len(errors)

    for actual_error, expected_error in zip(data["detail"], errors):
        assert expected_error.items() <= actual_error.items()


@pytest.mark.asyncio
async def test_create_user(client: httpx.AsyncClient) -> None:
    response = await client.post(
        "/auth/users/",
        json={
            "email": "john@doe.com",
            "full_name": "John Doe",
            "password": "p@ssw0rd",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert isinstance(data.pop("id"), int)
    assert data == {"email": "john@doe.com", "full_name": "John Doe"}


@pytest.mark.asyncio
async def test_create_user_already_exists(client: httpx.AsyncClient) -> None:
    response = await client.post(
        "/auth/users/",
        json={"email": "john@doe.com", "password": "somethingelse"},
    )
    assert response.status_code == 400


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "data",
    [
        pytest.param({}, id="empty"),
        pytest.param({"password": "s3kr3t"}, id="missing-email"),
        pytest.param({"email": "token@user.com"}, id="missing-password"),
    ],
)
async def test_token_create_invalid_payload(
    client: httpx.AsyncClient, data: dict
) -> None:
    response = await client.post("/auth/tokens/", json=data)
    assert response.status_code == 422


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "data",
    [
        pytest.param(
            {"email": "tawkun@user.com", "password": "s3kr3t"},
            id="user-does-not-exist",
        ),
        pytest.param(
            {"email": "token@user.com", "password": "wrong"},
            id="password-invalid",
        ),
    ],
)
async def test_token_create_invalid_credentials(
    client: httpx.AsyncClient, data: dict
) -> None:
    response = await client.post("/auth/tokens/", json=data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid credentials"


@pytest.mark.asyncio
async def test_token_create(client: httpx.AsyncClient) -> None:
    response = await client.post(
        "/auth/tokens/", json={"email": "token@user.com", "password": "s3kr3t"}
    )
    assert response.status_code == 201
    data = response.json()
    token = data["token"]

    response = await client.get(
        "/auth/check/", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json() == {"is_authenticated": True}


@pytest.mark.asyncio
async def test_cascade_user_is_kept_when_token_deleted(
    db: AsyncSession, temp_user: User
) -> None:
    email = temp_user.email  # Prevent stale read

    token, _ = await queries.get_or_create_token(db, user=temp_user)

    await queries.delete_token(db, token)

    assert await queries.get_token(db, token.key) is None
    assert await queries.get_user_by_email(db, email) == temp_user


@pytest.mark.asyncio
async def test_cascade_token_deleted_when_user_deleted(
    db: AsyncSession, temp_user: User
) -> None:
    email = temp_user.email  # Prevent stale read

    token, _ = await queries.get_or_create_token(db, user=temp_user)

    await queries.delete_user(db, temp_user)

    assert await queries.get_token(db, token.key) is None
    assert await queries.get_user_by_email(db, email) is None
