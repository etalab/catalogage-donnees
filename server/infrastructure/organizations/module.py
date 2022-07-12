from server.application.organizations.commands import CreateOrganization
from server.application.organizations.handlers import (
    create_organization,
    get_organization_by_siret,
)
from server.application.organizations.queries import GetOrganizationBySiret
from server.seedwork.application.modules import Module


class OrganizationsModule(Module):
    command_handlers = {
        CreateOrganization: create_organization,
    }

    query_handlers = {
        GetOrganizationBySiret: get_organization_by_siret,
    }
