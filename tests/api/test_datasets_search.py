import random
from contextlib import asynccontextmanager
from typing import AsyncIterator, List, Tuple

import httpx
import pytest

from server.application.datasets.commands import (
    CreateDataset,
    DeleteDataset,
    UpdateDataset,
)
from server.application.datasets.queries import GetDatasetByID
from server.config.di import resolve
from server.domain.datasets.entities import DataFormat, Dataset
from server.seedwork.application.messages import MessageBus

CORPUS_ITEMS = [
    ("Inventaire national forestier", "Ensemble des forêts de France"),
    ("Base Carbone", "Inventaire des données climat de l'ADEME"),
    ("Cadastre national", "Base de données du cadastre de la France"),
]


@asynccontextmanager
async def set_corpus(items: List[Tuple[str, str]]) -> AsyncIterator[None]:
    bus = resolve(MessageBus)

    datasets: List[Dataset] = []

    for title, description in items:
        command = CreateDataset(
            title=title, description=description, formats=[DataFormat.FILE_TABULAR]
        )
        pk = await bus.execute(command)
        query = GetDatasetByID(id=pk)
        dataset = await bus.execute(query)
        datasets.append(dataset)

    try:
        yield
    finally:
        for dataset in datasets:
            command = DeleteDataset(id=dataset.id)
            await bus.execute(command)


@pytest.fixture
async def default_corpus() -> AsyncIterator[None]:
    async with set_corpus(CORPUS_ITEMS):
        yield


@pytest.mark.asyncio
@pytest.mark.usefixtures("default_corpus")
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
    client: httpx.AsyncClient, q: str, expected_titles: List[str]
) -> None:
    response = await client.get("/datasets/", params={"q": q})
    assert response.status_code == 200
    data = response.json()
    titles = [item["title"] for item in data]
    assert titles == expected_titles


@pytest.mark.asyncio
@pytest.mark.usefixtures("default_corpus")
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
    client: httpx.AsyncClient, q_ref: str, q_other: str
) -> None:
    response = await client.get("/datasets/", params={"q": q_ref})
    assert response.status_code == 200
    data = response.json()
    reference_titles = [item["title"] for item in data]
    assert reference_titles

    response = await client.get("/datasets/", params={"q": q_other})
    assert response.status_code == 200
    data = response.json()
    other_titles = [item["title"] for item in data]

    assert reference_titles == other_titles


@pytest.mark.asyncio
@pytest.mark.usefixtures("default_corpus")
async def test_search_results_change_when_data_changes(
    client: httpx.AsyncClient,
) -> None:
    bus = resolve(MessageBus)

    # No results initially
    response = await client.get("/datasets/", params={"q": "titre"})
    assert response.status_code == 200
    data = response.json()
    assert not data

    # Add new dataset
    command = CreateDataset(
        title="Titre",
        description="Description",
        formats=[DataFormat.OTHER],
    )
    pk = await bus.execute(command)
    # New dataset is returned in search results
    response = await client.get("/datasets/", params={"q": "titre"})
    assert response.status_code == 200
    (dataset,) = response.json()
    assert dataset["id"] == str(pk)

    # Update dataset
    command = UpdateDataset(
        id=pk,
        title="Modifié",
        description="Description",
        formats=[DataFormat.OTHER],
    )
    await bus.execute(command)
    # Updated dataset is returned in search results targeting updated data
    response = await client.get("/datasets/", params={"q": "modifié"})
    assert response.status_code == 200
    (dataset,) = response.json()
    assert dataset["id"] == str(pk)

    # Same on description
    command = UpdateDataset(
        id=pk,
        title="Modifié",
        description="Jeu de données spécial",
        formats=[DataFormat.OTHER],
    )
    await bus.execute(command)
    response = await client.get("/datasets/", params={"q": "spécial"})
    assert response.status_code == 200
    (dataset,) = response.json()
    assert dataset["id"] == str(pk)

    # Deleted dataset is not returned in search results anymore
    command = DeleteDataset(id=pk)
    await bus.execute(command)
    response = await client.get("/datasets/", params={"q": "modifié"})
    assert response.status_code == 200
    data = response.json()
    assert not data


@pytest.mark.asyncio
async def test_search_ranking(client: httpx.AsyncClient) -> None:
    items = [
        ("A", "..."),
        ("B", "Forêt nouvelle"),
        ("C", "Historique des forêts anciennes"),
        ("D", "Ancien historique des forêts"),
        ("E", "Historique des forêts anciennes reste du document"),
    ]

    random.shuffle(items)  # Ensure DB insert order is irrelevant.

    q = "Forêt ancienne"

    expected_titles = [
        "E",  # Both lexemes match, in the same order, earlier in the document
        "C",  # Both lexemes match, in the same order
        "D",  # Both lexemes match, but in different order
    ]

    async with set_corpus(items):
        response = await client.get("/datasets/", params={"q": q})
        assert response.status_code == 200
        data = response.json()
        titles = [item["title"] for item in data]
        assert titles == expected_titles
