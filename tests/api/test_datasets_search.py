from typing import AsyncIterator, List

import httpx
import pytest

from server.application.datasets.commands import CreateDataset, DeleteDataset
from server.application.datasets.queries import GetDatasetByID
from server.config.di import resolve
from server.domain.datasets.entities import DataFormat, Dataset
from server.seedwork.application.messages import MessageBus

CORPUS_ITEMS = [
    ("Inventaire national forestier", "Ensemble des forêts de France"),
    ("Base Carbone", "Inventaire des données climat de l'ADEME"),
    ("Cadastre national", "Base de données du cadastre de la France"),
]


@pytest.fixture(autouse=True, scope="module")
async def corpus() -> AsyncIterator[None]:
    bus = resolve(MessageBus)

    datasets: List[Dataset] = []

    for title, description in CORPUS_ITEMS:
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


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "q, expected_titles",
    [
        pytest.param("", [], id="empty-search"),
        pytest.param("tototitu", [], id="no-results"),
        pytest.param(
            "carbone",
            ["Base Carbone"],
            id="single-result-title",
        ),
        pytest.param(
            "forêt",
            ["Inventaire national forestier"],
            id="single-result-description",
        ),
        pytest.param(
            "national",
            ["Inventaire national forestier", "Cadastre national"],
            id="many-results-title",
        ),
        pytest.param(
            "France",
            ["Inventaire national forestier", "Cadastre national"],
            id="many-results-description",
        ),
        pytest.param(
            "base",
            ["Base Carbone", "Cadastre national"],
            id="many-results-title-description",
        ),
    ],
)
async def test_search_empty(
    client: httpx.AsyncClient, q: str, expected_titles: List[str]
) -> None:
    response = await client.get("/datasets/", params={"q": q})
    assert response.status_code == 200
    data = response.json()
    titles = [item["title"] for item in data]
    assert titles == expected_titles
