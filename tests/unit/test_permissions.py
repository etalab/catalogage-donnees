import httpx
import pytest
from xpresso import App, Depends, Path

from server.api.auth.dependencies import HasRole, IsAuthenticated
from server.domain.auth.entities import UserRole

from ..helpers import TestUser


@pytest.mark.asyncio
async def test_is_authenticated(temp_user: TestUser) -> None:
    app = App(
        routes=[
            Path(
                "/",
                get=lambda: "OK",
                dependencies=[Depends(IsAuthenticated())],
            ),
        ],
    )

    async with httpx.AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.get("/")
        assert response.status_code == 401

        headers = {"Authorization": f"Bearer {temp_user.api_token}"}
        response = await client.get("/", headers=headers)
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_has_role(temp_user: TestUser, admin_user: TestUser) -> None:
    app = App(
        routes=[
            Path(
                "/",
                get=lambda: "OK",
                dependencies=[Depends(HasRole(UserRole.ADMIN))],
            ),
        ],
    )

    async with httpx.AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.get("/")
        assert response.status_code == 401

        headers = {"Authorization": f"Bearer {temp_user.api_token}"}
        response = await client.get("/", headers=headers)
        assert response.status_code == 403

        headers = {"Authorization": f"Bearer {admin_user.api_token}"}
        response = await client.get("/", headers=headers)
        assert response.status_code == 200
