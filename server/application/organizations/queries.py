from server.domain.organizations.types import Siret
from server.seedwork.application.queries import Query

from .views import OrganizationView


class GetOrganizationBySiret(Query[OrganizationView]):
    siret: Siret
