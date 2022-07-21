from server.seedwork.domain.entities import Entity

from ..organizations.types import Siret


class Catalog(Entity):
    organization_siret: Siret
