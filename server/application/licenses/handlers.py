from typing import List

from server.config.di import resolve
from server.domain.datasets.repositories import DatasetRepository
from server.domain.licenses.entities import BUILTIN_LICENSE_SUGGESTIONS

from .queries import GetLicenseSet


async def get_license_set(query: GetLicenseSet) -> List[str]:
    repository = resolve(DatasetRepository)
    stored_licenses = await repository.get_license_set()
    return sorted(BUILTIN_LICENSE_SUGGESTIONS | stored_licenses)
