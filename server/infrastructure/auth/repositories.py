from typing import Optional

from sqlalchemy import Column, Enum, Integer, String, delete, insert, select
from sqlalchemy.exc import NoResultFound

from server.domain.auth.entities import User, UserRole
from server.domain.auth.repositories import UserRepository
from server.domain.common.types import ID

from ..database import Base, Database


class UserModel(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False, unique=True, index=True)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.USER)


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

    async def insert(self, entity: User) -> ID:
        async with self._db.session() as session:
            stmt = insert(UserModel).values(**entity.dict()).returning(UserModel.id)
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar_one()

    async def delete(self, id: ID) -> None:
        async with self._db.session() as session:
            stmt = delete(UserModel).where(UserModel.id == id)
            await session.execute(stmt)
            await session.commit()
