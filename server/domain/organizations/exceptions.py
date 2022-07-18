from ..common.exceptions import DoesNotExist
from .entities import Organization


class OrganizationDoesNotExist(DoesNotExist):
    entity_name = "Organization"


class OrganizationAlreadyExists(Exception):
    def __init__(self, organization: Organization) -> None:
        super().__init__()
        self.organization = organization
