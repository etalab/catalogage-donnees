from dataclasses import dataclass
from typing import Callable

import httpx
import pytest

from server.config.di import resolve
from server.domain.common.types import ID, id_factory
from server.domain.datasets.entities import DataFormat, GeographicalCoverage
from server.seedwork.application.messages import MessageBus

from ..factories import CreateDatasetFactory, CreateTagFactory
from ..helpers import TestUser


@pytest.mark.asyncio
async def test_dataset_filters_info(
    client: httpx.AsyncClient, temp_user: TestUser
) -> None:
    bus = resolve(MessageBus)

    tag_id = await bus.execute(CreateTagFactory.build(name="Architecture"))

    await bus.execute(
        CreateDatasetFactory.build(
            service="Same example service",
            technical_source="Example database system",
        )
    )

    # Add another with filterable optional fields left out
    await bus.execute(
        CreateDatasetFactory.build(
            service="Same example service",
            technical_source=None,
        )
    )

    response = await client.get("/datasets/filters/", auth=temp_user.auth)
    assert response.status_code == 200

    data = response.json()

    assert set(data) == {
        "geographical_coverage",
        "service",
        "format",
        "technical_source",
        "tag_id",
    }

    assert sorted(data["geographical_coverage"]) == [
        "department",
        "epci",
        "europe",
        "municipality",
        "national",
        "national_full_territory",
        "region",
        "world",
    ]

    assert data["service"] == [
        "Same example service",
    ]

    assert sorted(data["format"]) == [
        "api",
        "database",
        "file_gis",
        "file_tabular",
        "other",
        "website",
    ]

    assert data["technical_source"] == [
        "Example database system",
    ]

    assert data["tag_id"] == [
        {"id": str(tag_id), "name": "Architecture"},
    ]


@dataclass
class _Env:
    tag_id: ID


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "filtername, create_kwargs, negative_value, positive_value",
    [
        pytest.param(
            "geographical_coverage",
            lambda _: {"geographical_coverage": GeographicalCoverage.NATIONAL.value},
            lambda _: [GeographicalCoverage.REGION.value],
            lambda _: [GeographicalCoverage.NATIONAL.value],
            id="geographical_coverage",
        ),
        pytest.param(
            "service",
            lambda _: {"service": "Service cartes"},
            lambda _: ["Autre direction"],
            lambda _: ["Service cartes"],
            id="service",
        ),
        pytest.param(
            "format",
            lambda _: {"formats": [DataFormat.FILE_GIS.value]},
            lambda _: [DataFormat.DATABASE.value],
            lambda _: [DataFormat.FILE_GIS.value],
            id="format",
        ),
        pytest.param(
            "technical_source",
            lambda _: {"technical_source": "SGBD central"},
            lambda _: ["Autre système"],
            lambda _: ["SGBD central"],
            id="technical_source",
        ),
        pytest.param(
            "tag_id",
            lambda env: {"tag_ids": [env.tag_id]},
            lambda _: [str(id_factory())],
            lambda env: [str(env.tag_id)],
            id="tag_id",
        ),
    ],
)
async def test_dataset_filters_apply(
    client: httpx.AsyncClient,
    temp_user: TestUser,
    filtername: str,
    create_kwargs: Callable[[_Env], dict],
    positive_value: Callable[[_Env], list],
    negative_value: Callable[[_Env], list],
) -> None:
    bus = resolve(MessageBus)

    tag_id = await bus.execute(CreateTagFactory.build())
    env = _Env(tag_id=tag_id)

    dataset_id = await bus.execute(CreateDatasetFactory.build(**create_kwargs(env)))

    params = {filtername: negative_value(env)}
    response = await client.get("/datasets/", params=params, auth=temp_user.auth)
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 0

    params = {filtername: positive_value(env)}
    response = await client.get("/datasets/", params=params, auth=temp_user.auth)
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 1
    assert data["items"][0]["id"] == str(dataset_id)
