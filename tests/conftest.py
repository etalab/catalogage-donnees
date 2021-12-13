from typing import AsyncIterator

import httpx
import pytest

from server.app import create_app


@pytest.fixture
async def client() -> AsyncIterator[httpx.AsyncClient]:
    app = create_app()

    async with httpx.AsyncClient(app=app, base_url="http://testserver") as client:
        yield client
