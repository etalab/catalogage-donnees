from typing import Optional

from server.domain.organizations.types import Siret
from server.seedwork.domain.repositories import Repository

from .entities import Organization


class OrganizationRepository(Repository):
    async def get_by_siret(self, siret: Siret) -> Optional[Organization]:
        raise NotImplementedError  # pragma: no cover

    async def insert(self, entity: Organization) -> Siret:
        raise NotImplementedError  # pragma: no cover
