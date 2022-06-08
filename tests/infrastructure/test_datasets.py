import pytest
from sqlalchemy import select
from sqlalchemy.orm import contains_eager

from server.application.datasets.commands import CreateDataset, DeleteDataset
from server.application.datasets.queries import GetDatasetByID
from server.application.tags.commands import CreateTag
from server.config.di import resolve
from server.domain.catalog_records.repositories import CatalogRecordRepository
from server.domain.datasets.entities import DataFormat, GeographicalCoverage
from server.infrastructure.database import Database
from server.infrastructure.datasets.repositories import DatasetModel
from server.infrastructure.tags.repositories import TagModel, dataset_tag
from server.seedwork.application.messages import MessageBus


@pytest.mark.asyncio
async def test_dataset_cascades() -> None:
    bus = resolve(MessageBus)

    tag_architecture_id = await bus.execute(CreateTag(name="Architecture"))

    dataset_id = await bus.execute(
        CreateDataset(
            title="Title",
            description="Description",
            service="Example service",
            geographical_coverage=GeographicalCoverage.NATIONAL,
            formats=[DataFormat.WEBSITE, DataFormat.API],
            contact_emails=["person@mydomain.org"],
            tag_ids=[str(tag_architecture_id)],
        )
    )

    dataset = await bus.execute(GetDatasetByID(id=dataset_id))

    await bus.execute(DeleteDataset(id=dataset_id))

    # - Catalog record has been deleted.
    catalog_record_repository = resolve(CatalogRecordRepository)
    assert await catalog_record_repository.get_by_id(dataset.catalog_record.id) is None

    # - Tags have been disconnected from dataset, and still exist.
    async with resolve(Database).session() as session:
        stmt = (
            select(TagModel)
            .join(dataset_tag, isouter=True)
            .join(DatasetModel, isouter=True)
            .options(contains_eager(TagModel.datasets))
            .where(TagModel.id == tag_architecture_id)
        )
        result = await session.execute(stmt)
        tag = result.unique().scalar_one()
        assert tag.name == "Architecture"
        assert not tag.datasets
