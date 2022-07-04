import httpx
import pytest


@pytest.mark.asyncio
async def test_index(client: httpx.AsyncClient) -> None:
    response = await client.get("/")
    assert response.status_code == 307
    assert response.headers["Location"] == "http://testserver/docs"


@pytest.mark.asyncio
async def test_api_docs(client: httpx.AsyncClient) -> None:
    response = await client.get("/docs")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_openapi(client: httpx.AsyncClient) -> None:
    response = await client.get("/openapi.json")
    assert response.status_code == 200
    schema = response.json()

    # HTTP Bearer security scheme must be registered.
    bearer_scheme = schema["components"]["securitySchemes"].get("Bearer")
    assert bearer_scheme is not None
    assert bearer_scheme["type"] == "http"
    assert bearer_scheme["scheme"] == "bearer"

    # Authenticated endpoints must be tied to the HTTP Bearer scheme.
    # We just take an exmaple endpoint here.
    assert {"Bearer": []} in schema["paths"]["/auth/users/"]["post"]["security"]


@pytest.mark.parametrize("origin", ["http://localhost:3000"])
@pytest.mark.asyncio
async def test_cors(client: httpx.AsyncClient, origin: str) -> None:
    headers = {
        "Origin": origin,
        "Access-Control-Request-Method": "POST",
        "Access-Control-Request-Headers": "Content-Type",
    }
    response = await client.options("/", headers=headers)
    assert response.status_code == 200
    assert response.headers["Access-Control-Allow-Origin"] == origin
    assert "POST" in response.headers["Access-Control-Allow-Methods"]
    assert response.headers["Access-Control-Allow-Credentials"]
    assert response.headers["Access-Control-Allow-Headers"] == "Content-Type"


@pytest.mark.asyncio
async def test_cors_disallowed_origin(client: httpx.AsyncClient) -> None:
    headers = {
        "Origin": "http://disallowed.com",
        "Access-Control-Request-Method": "POST",
        "Access-Control-Request-Headers": "Content-Type",
    }
    response = await client.options("/", headers=headers)
    assert response.status_code == 400
