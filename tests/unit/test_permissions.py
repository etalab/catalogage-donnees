import httpx
import pytest
from fastapi import Depends, FastAPI

from server.api.auth.backends.token import TokenAuthBackend
from server.api.auth.dependencies import HasRole, IsAuthenticated
from server.api.auth.middleware import AuthMiddleware
from server.domain.auth.entities import UserRole

from ..helpers import TestUser


@pytest.mark.asyncio
async def test_is_authenticated(temp_user: TestUser) -> None:
    app = FastAPI()

    app.add_middleware(AuthMiddleware, backend=TokenAuthBackend())

    @app.get("/", dependencies=[Depends(IsAuthenticated())])
    async def index() -> str:
        return "OK"

    async with httpx.AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.get("/")
        assert response.status_code == 401

        headers = {"Authorization": f"Bearer {temp_user.api_token}"}
        response = await client.get("/", headers=headers)
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_has_role(temp_user: TestUser, admin_user: TestUser) -> None:
    app = FastAPI()

    app.add_middleware(AuthMiddleware, backend=TokenAuthBackend())

    @app.get(
        "/", dependencies=[Depends(IsAuthenticated()), Depends(HasRole(UserRole.ADMIN))]
    )
    async def index() -> str:
        return "OK"

    async with httpx.AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.get("/")
        assert response.status_code == 401

        headers = {"Authorization": f"Bearer {temp_user.api_token}"}
        response = await client.get("/", headers=headers)
        assert response.status_code == 403

        headers = {"Authorization": f"Bearer {admin_user.api_token}"}
        response = await client.get("/", headers=headers)
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_has_role_requires_is_authenticated() -> None:
    app = FastAPI()

    app.add_middleware(AuthMiddleware, backend=TokenAuthBackend())

    @app.get(
        "/",
        dependencies=[
            # 'Depends(IsAuthenticated()),' missing here.
            Depends(HasRole(UserRole.ADMIN)),
        ],
    )
    async def index() -> str:
        return "OK"

    async with httpx.AsyncClient(app=app, base_url="http://testserver") as client:
        with pytest.raises(RuntimeError, match="IsAuthenticated"):
            await client.get("/")
