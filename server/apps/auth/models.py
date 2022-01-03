import secrets
from typing import Optional

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from server.db import Base

from . import passwords


class User(Base):
    __tablename__ = "user"

    id: int = Column(Integer, primary_key=True, index=True)
    email: str = Column(String, nullable=False, unique=True, index=True)
    password_hash: str = Column(String, nullable=False)
    full_name: Optional[str] = Column(String)
    token: "Token" = relationship(
        "Token",
        uselist=False,
        back_populates="user",
        cascade="all, delete",
    )

    def set_password(self, password: str) -> None:
        self.password_hash = passwords.hash(password)

    def check_password(self, password: str) -> bool:
        return passwords.verify(password, self.password_hash)

    def __repr__(self) -> str:
        return f"<User {self.email}>"


class Token(Base):
    __tablename__ = "token"

    key: str = Column(String, primary_key=True)
    user_id: int = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))
    user: "User" = relationship("User", back_populates="token")


def make_token_key() -> str:
    return secrets.token_hex(20)
