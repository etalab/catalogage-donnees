import random
from typing import List, Optional, Tuple

import httpx
import pytest

from server.application.datasets.commands import (
    CreateDataset,
    DeleteDataset,
    UpdateDataset,
)
from server.application.datasets.queries import GetDatasetByID
from server.config.di import resolve
from server.domain.datasets.entities import DataFormat, GeographicalCoverage
from server.seedwork.application.messages import MessageBus

from ..helpers import TestUser

DEFAULT_CORPUS_ITEMS = [
    ("Inventaire national forestier", "Ensemble des forêts de France"),
    ("Base Carbone", "Inventaire des données climat de l'ADEME"),
    ("Cadastre national", "Base de données du cadastre de la France"),
]


async def add_corpus(items: List[Tuple[str, str]] = None) -> None:
    if items is None:
        items = DEFAULT_CORPUS_ITEMS

    bus = resolve(MessageBus)

    for title, description in items:
        command = CreateDataset(
            title=title,
            description=description,
            service="Service",
            geographical_coverage=GeographicalCoverage.NATIONAL,
            formats=[DataFormat.FILE_TABULAR],
            entrypoint_email="service@mydomain.org",
        )
        pk = await bus.execute(command)
        query = GetDatasetByID(id=pk)
        await bus.execute(query)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "q, expected_titles",
    [
        pytest.param(
            "",
            [],
            id="terms:none",
        ),
        pytest.param(
            "hello!? hm?m & || specia| ch@rs'); \"quote",
            [],
            id="terms:garbage",
        ),
        pytest.param(
            "tototitu",
            [],
            id="terms:single-results:none",
        ),
        pytest.param(
            "carbone",
            ["Base Carbone"],
            id="terms:single-result:single-title",
        ),
        pytest.param(
            "forêt",
            ["Inventaire national forestier"],
            id="terms:single-result:single-description",
        ),
        pytest.param(
            "national",
            ["Inventaire national forestier", "Cadastre national"],
            id="terms:single-results:multiple-title",
        ),
        pytest.param(
            "France",
            ["Inventaire national forestier", "Cadastre national"],
            id="terms:single-results:multiple-description",
        ),
        pytest.param(
            "base",
            ["Base Carbone", "Cadastre national"],
            id="terms:single-results:multiple-title-description",
        ),
        pytest.param(
            "données cadastre",
            ["Cadastre national"],
            id="terms:multiple-results:single",
        ),
    ],
)
async def test_search(
    client: httpx.AsyncClient, temp_user: TestUser, q: str, expected_titles: List[str]
) -> None:
    await add_corpus()

    response = await client.get(
        "/datasets/",
        params={"q": q},
        auth=temp_user.auth,
    )
    assert response.status_code == 200
    data = response.json()
    titles = [item["title"] for item in data]
    assert titles == expected_titles


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "q_ref, q_other",
    [
        pytest.param(
            "forêt",
            "forestier",
            id="lexemes",
        ),
        pytest.param(
            "base",
            "BaSe",
            id="case-insensitive",
        ),
    ],
)
async def test_search_robustness(
    client: httpx.AsyncClient, temp_user: TestUser, q_ref: str, q_other: str
) -> None:
    await add_corpus()

    response = await client.get(
        "/datasets/",
        params={"q": q_ref},
        auth=temp_user.auth,
    )
    assert response.status_code == 200
    data = response.json()
    reference_titles = [item["title"] for item in data]
    assert reference_titles

    response = await client.get(
        "/datasets/",
        params={"q": q_other},
        auth=temp_user.auth,
    )
    assert response.status_code == 200
    data = response.json()
    other_titles = [item["title"] for item in data]

    assert reference_titles == other_titles


@pytest.mark.asyncio
async def test_search_results_change_when_data_changes(
    client: httpx.AsyncClient,
    temp_user: TestUser,
) -> None:
    await add_corpus()

    bus = resolve(MessageBus)

    # No results initially
    response = await client.get(
        "/datasets/",
        params={"q": "titre"},
        auth=temp_user.auth,
    )
    assert response.status_code == 200
    data = response.json()
    assert not data

    # Add new dataset
    command = CreateDataset(
        title="Titre",
        description="Description",
        service="Service",
        geographical_coverage=GeographicalCoverage.DEPARTMENT,
        formats=[DataFormat.OTHER],
        entrypoint_email="service@mydomain.org",
    )
    pk = await bus.execute(command)
    # New dataset is returned in search results
    response = await client.get(
        "/datasets/",
        params={"q": "titre"},
        auth=temp_user.auth,
    )
    assert response.status_code == 200
    (dataset,) = response.json()
    assert dataset["id"] == str(pk)

    # Update dataset title
    command = UpdateDataset(
        id=pk,
        title="Modifié",
        description="Description",
        service="Service",
        geographical_coverage=GeographicalCoverage.DEPARTMENT,
        formats=[DataFormat.OTHER],
        technical_source=None,
        entrypoint_email="service@mydomain.org",
        contact_emails=[],
        update_frequency=None,
        last_updated_at=None,
    )
    await bus.execute(command)
    # Updated dataset is returned in search results targeting updated data
    response = await client.get(
        "/datasets/",
        params={"q": "modifié"},
        auth=temp_user.auth,
    )
    assert response.status_code == 200
    (dataset,) = response.json()
    assert dataset["id"] == str(pk)

    # Same on description
    command = UpdateDataset(
        id=pk,
        title="Modifié",
        description="Jeu de données spécial",
        service="Service",
        geographical_coverage=GeographicalCoverage.DEPARTMENT,
        formats=[DataFormat.OTHER],
        technical_source=None,
        entrypoint_email="service@mydomain.org",
        contact_emails=[],
        update_frequency=None,
        last_updated_at=None,
    )
    await bus.execute(command)
    response = await client.get(
        "/datasets/",
        params={"q": "spécial"},
        auth=temp_user.auth,
    )
    assert response.status_code == 200
    (dataset,) = response.json()
    assert dataset["id"] == str(pk)

    # Deleted dataset is not returned in search results anymore
    command = DeleteDataset(id=pk)
    await bus.execute(command)
    response = await client.get(
        "/datasets/",
        params={"q": "modifié"},
        auth=temp_user.auth,
    )
    assert response.status_code == 200
    data = response.json()
    assert not data


@pytest.mark.asyncio
async def test_search_ranking(client: httpx.AsyncClient, temp_user: TestUser) -> None:
    items = [
        ("A", "..."),
        ("B", "Forêt nouvelle"),
        ("C", "Historique des forêts anciennes"),
        ("D", "Ancien historique des forêts"),
    ]

    random.shuffle(items)  # Ensure DB insert order is irrelevant.

    await add_corpus(items)

    q = "Forêt ancienne"  # Lexemes: forêt, ancien

    expected_titles = [
        "C",  # Both lexemes match, close to each other
        "D",  # Both lexemes match, further away from each other
    ]

    response = await client.get("/datasets/", params={"q": q}, auth=temp_user.auth)
    assert response.status_code == 200
    data = response.json()
    titles = [item["title"] for item in data]
    assert titles == expected_titles


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "highlight, expected_headlines",
    [
        pytest.param(
            False,
            None,
            id="off",
        ),
        pytest.param(
            True,
            {
                "title": "<mark>Restaurants</mark> CROUS",
                "description": "Lieux de <mark>restauration</mark> du CROUS",
            },
            id="on",
        ),
    ],
)
async def test_search_highlight(
    client: httpx.AsyncClient,
    temp_user: TestUser,
    highlight: bool,
    expected_headlines: Optional[dict],
) -> None:
    await add_corpus([("Restaurants CROUS", "Lieux de restauration du CROUS")])

    q = "restaurant"

    response = await client.get(
        "/datasets/",
        params={"q": q, "highlight": highlight},
        auth=temp_user.auth,
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1

    assert data[0]["headlines"] == expected_headlines
