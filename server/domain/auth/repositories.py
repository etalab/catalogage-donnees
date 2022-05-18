from typing import Optional

from server.seedwork.domain.repositories import Repository

from ..common.types import ID, id_factory
from .entities import User


class UserRepository(Repository):
    def make_id(self) -> ID:
        return id_factory()

    async def get_by_email(self, email: str) -> Optional[User]:
        raise NotImplementedError  # pragma: no cover

    async def get_by_api_token(self, api_token: str) -> Optional[User]:
        raise NotImplementedError  # pragma: no cover

    async def insert(self, entity: User) -> ID:
        raise NotImplementedError  # pragma: no cover

    async def update(self, entity: User) -> None:
        raise NotImplementedError  # pragma: no cover

    async def delete(self, id: ID) -> None:
        raise NotImplementedError  # pragma: no cover
