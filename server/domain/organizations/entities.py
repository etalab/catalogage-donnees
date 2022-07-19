from server.seedwork.domain.entities import Entity

from .types import Siret


class Organization(Entity):
    name: str
    siret: Siret


# A fake SIRET used for the organization that holds legacy users and whose catalog holds
# legacy datasets. "Legacy" means "before the multi-org system powered by DataPass.
# Going forward SIRET numbers will come from DataPass via the user's organization(s).
LEGACY_ORGANIZATION_SIRET = Siret("000 000 000 00000")
