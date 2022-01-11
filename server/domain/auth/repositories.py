from typing import Optional

from server.seedwork.domain.repositories import Repository

from ..common.types import ID
from .entities import User


class UserRepository(Repository):
    async def get_by_email(self, email: str) -> Optional[User]:
        raise NotImplementedError

    async def insert(self, entity: User) -> ID:
        raise NotImplementedError

    async def delete(self, id: ID) -> None:
        raise NotImplementedError
