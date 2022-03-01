import uuid
from typing import Optional

from sqlalchemy import Column, String, delete, select
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.exc import NoResultFound

from server.application.auth.passwords import API_TOKEN_LENGTH
from server.domain.auth.entities import User
from server.domain.auth.repositories import UserRepository
from server.domain.common.types import ID

from ..database import Base, Database


class UserModel(Base):
    __tablename__ = "user"

    id: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True)
    email = Column(String, nullable=False, unique=True, index=True)
    password_hash = Column(String, nullable=False)
    api_token = Column(String(API_TOKEN_LENGTH), nullable=False)


class SqlUserRepository(UserRepository):
    def __init__(self, db: Database) -> None:
        self._db = db

    async def get_by_email(self, email: str) -> Optional[User]:
        async with self._db.session() as session:
            stmt = select(UserModel).where(UserModel.email == email)
            result = await session.execute(stmt)
            try:
                obj = result.scalar_one()
            except NoResultFound:
                return None
            else:
                return User.from_orm(obj)

    async def get_by_api_token(self, api_token: str) -> Optional[User]:
        async with self._db.session() as session:
            stmt = select(UserModel).where(UserModel.api_token == api_token)
            result = await session.execute(stmt)
            try:
                obj = result.scalar_one()
            except NoResultFound:
                return None
            else:
                return User.from_orm(obj)

    async def insert(self, entity: User) -> ID:
        async with self._db.session() as session:
            instance = UserModel(
                id=entity.id,
                email=entity.email,
                password_hash=entity.password_hash,
                api_token=entity.api_token,
            )

            session.add(instance)

            await session.commit()
            await session.refresh(instance)

            return ID(instance.id)

    async def delete(self, id: ID) -> None:
        async with self._db.session() as session:
            stmt = delete(UserModel).where(UserModel.id == id)
            await session.execute(stmt)
            await session.commit()
