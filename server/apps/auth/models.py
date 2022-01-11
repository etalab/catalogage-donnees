from sqlalchemy import Column, Integer, String

from server.db import Base


class User(Base):
    __tablename__ = "user"

    id: int = Column(Integer, primary_key=True, index=True)
    email: str = Column(String, nullable=False, unique=True, index=True)

    def __repr__(self) -> str:
        return f"<User {self.email}>"
