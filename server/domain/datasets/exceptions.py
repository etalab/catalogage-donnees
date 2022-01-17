from ..common.exceptions import DoesNotExist


class DatasetDoesNotExist(DoesNotExist):
    entity_name = "Dataset"
