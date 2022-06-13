from server.application.datasets.commands import (
    CreateDataset,
    DeleteDataset,
    UpdateDataset,
)
from server.application.datasets.handlers import (
    create_dataset,
    delete_dataset,
    get_all_datasets,
    get_dataset_by_id,
    get_dataset_filters,
    update_dataset,
)
from server.application.datasets.queries import (
    GetAllDatasets,
    GetDatasetByID,
    GetDatasetFilters,
)
from server.seedwork.application.modules import Module


class DatasetsModule(Module):
    command_handlers = {
        CreateDataset: create_dataset,
        UpdateDataset: update_dataset,
        DeleteDataset: delete_dataset,
    }

    query_handlers = {
        GetAllDatasets: get_all_datasets,
        GetDatasetByID: get_dataset_by_id,
        GetDatasetFilters: get_dataset_filters,
    }
