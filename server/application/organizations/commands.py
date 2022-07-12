from server.domain.organizations.types import Siret
from server.seedwork.application.commands import Command


class CreateOrganization(Command[Siret]):
    name: str
    siret: Siret
