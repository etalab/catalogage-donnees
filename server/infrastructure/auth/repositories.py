import uuid
from typing import Any, Optional

from sqlalchemy import Column, Enum, String, select
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from server.application.auth.passwords import API_TOKEN_LENGTH
from server.domain.auth.entities import User, UserRole
from server.domain.auth.exceptions import UserDoesNotExist
from server.domain.auth.repositories import UserRepository
from server.domain.common.types import ID
from server.infrastructure.deletion.helpers import soft_delete

from ..database import Base, Database


class UserModel(Base):
    __tablename__ = "user"

    id: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True)
    email = Column(String, nullable=False, unique=True, index=True)
    password_hash = Column(String, nullable=False)
    role = Column(Enum(UserRole, name="user_role_enum"), nullable=False)
    api_token = Column(String(API_TOKEN_LENGTH), nullable=False)


def update_instance(instance: UserModel, entity: User) -> None:
    for field in set(User.__fields__) - {"id"}:
        setattr(instance, field, getattr(entity, field))


class SqlUserRepository(UserRepository):
    def __init__(self, db: Database) -> None:
        self._db = db

    async def _maybe_get_by(
        self, session: AsyncSession, **kwargs: Any
    ) -> Optional[UserModel]:
        whereclauses = (
            getattr(UserModel, column) == value for column, value in kwargs.items()
        )
        stmt = select(UserModel).where(*whereclauses)
        result = await session.execute(stmt)
        try:
            return result.scalar_one()
        except NoResultFound:
            return None

    async def get_by_email(self, email: str) -> Optional[User]:
        async with self._db.session() as session:
            instance = await self._maybe_get_by(session, email=email)

            if instance is None:
                return None

            return User.from_orm(instance)

    async def get_by_api_token(self, api_token: str) -> Optional[User]:
        async with self._db.session() as session:
            instance = await self._maybe_get_by(session, api_token=api_token)

            if instance is None:
                return None

            return User.from_orm(instance)

    async def insert(self, entity: User) -> ID:
        async with self._db.session() as session:
            instance = UserModel(
                id=entity.id,
                email=entity.email,
                password_hash=entity.password_hash,
                role=entity.role,
                api_token=entity.api_token,
            )

            session.add(instance)

            await session.commit()
            await session.refresh(instance)

            return ID(instance.id)

    async def update(self, entity: User) -> None:
        async with self._db.session() as session:
            instance = await self._maybe_get_by(session, id=entity.id)

            if instance is None:
                raise UserDoesNotExist(entity.email)

            update_instance(instance, entity)

            await session.commit()

    async def delete(self, id: ID) -> None:
        async with self._db.session() as session:
            user = await self._maybe_get_by(session, id=id)

            if user is None:
                return

            await soft_delete(session, user)
            await session.commit()
