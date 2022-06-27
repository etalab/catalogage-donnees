from server.application.tags.queries import GetAllTags
from server.config.di import resolve
from server.domain.catalog_records.entities import CatalogRecord
from server.domain.catalog_records.repositories import CatalogRecordRepository
from server.domain.common.pagination import Pagination
from server.domain.common.types import ID
from server.domain.datasets.entities import DataFormat, Dataset, GeographicalCoverage
from server.domain.datasets.exceptions import DatasetDoesNotExist
from server.domain.datasets.repositories import DatasetRepository
from server.domain.tags.repositories import TagRepository
from server.seedwork.application.messages import MessageBus

from .commands import CreateDataset, DeleteDataset, UpdateDataset
from .queries import GetAllDatasets, GetDatasetByID, GetDatasetFilters
from .views import DatasetFiltersView, DatasetView


async def create_dataset(command: CreateDataset, *, id_: ID = None) -> ID:
    repository = resolve(DatasetRepository)
    catalog_record_repository = resolve(CatalogRecordRepository)
    tag_repository = resolve(TagRepository)

    if id_ is None:
        id_ = repository.make_id()

    catalog_record_id = await catalog_record_repository.insert(
        CatalogRecord(id=catalog_record_repository.make_id())
    )
    catalog_record = await catalog_record_repository.get_by_id(catalog_record_id)
    assert catalog_record is not None

    tags = await tag_repository.get_all(ids=command.tag_ids)

    dataset = Dataset(
        id=id_,
        catalog_record=catalog_record,
        tags=tags,
        **command.dict(exclude={"tag_ids"}),
    )

    return await repository.insert(dataset)


async def update_dataset(command: UpdateDataset) -> None:
    repository = resolve(DatasetRepository)
    tag_repository = resolve(TagRepository)

    pk = command.id
    dataset = await repository.get_by_id(pk)
    if dataset is None:
        raise DatasetDoesNotExist(pk)

    tags = await tag_repository.get_all(ids=command.tag_ids)
    dataset.update(**command.dict(exclude={"id", "tag_ids"}), tags=tags)

    await repository.update(dataset)


async def delete_dataset(command: DeleteDataset) -> None:
    repository = resolve(DatasetRepository)
    await repository.delete(command.id)


async def get_dataset_filters(query: GetDatasetFilters) -> DatasetFiltersView:
    bus = resolve(MessageBus)
    repository = resolve(DatasetRepository)

    services = await repository.get_service_set()
    technical_sources = await repository.get_technical_source_set()
    tags = await bus.execute(GetAllTags())

    return DatasetFiltersView(
        geographical_coverage=list(GeographicalCoverage),
        service=list(services),
        format=list(DataFormat),
        technical_source=list(technical_sources),
        tag_id=[tag.id for tag in tags],
    )


async def get_all_datasets(query: GetAllDatasets) -> Pagination[DatasetView]:
    repository = resolve(DatasetRepository)

    datasets, count = await repository.get_all(page=query.page, spec=query.spec)

    views = [DatasetView(**dataset.dict(), **extras) for dataset, extras in datasets]

    return Pagination(items=views, total_items=count, page_size=query.page.size)


async def get_dataset_by_id(query: GetDatasetByID) -> DatasetView:
    repository = resolve(DatasetRepository)

    id = query.id
    dataset = await repository.get_by_id(id)

    if dataset is None:
        raise DatasetDoesNotExist(id)

    return DatasetView(**dataset.dict())
