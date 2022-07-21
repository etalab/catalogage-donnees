from pydantic import EmailStr, SecretStr

from server.domain.common.types import ID
from server.domain.organizations.entities import LEGACY_ORGANIZATION_SIRET
from server.domain.organizations.types import Siret
from server.seedwork.application.commands import Command


class CreateUser(Command[ID]):
    organization_siret: Siret = LEGACY_ORGANIZATION_SIRET
    email: EmailStr
    password: SecretStr


class DeleteUser(Command[None]):
    id: ID


class ChangePassword(Command[None]):
    email: EmailStr
    password: SecretStr
