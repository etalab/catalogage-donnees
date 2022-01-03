from typing import Optional, Tuple

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from .models import Token, User, make_token_key


async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    stmt = select(User).where(User.email == email)
    result = await db.execute(stmt)
    return result.scalars().first()


async def create_user(
    db: AsyncSession, *, email: str, password: str, full_name: str = None
) -> User:
    user = User(email=email, full_name=full_name)
    user.set_password(password)

    db.add(user)
    await db.commit()
    await db.refresh(user)

    return user


async def delete_user(db: AsyncSession, user: User) -> None:
    await db.delete(user)
    await db.commit()


async def get_token(db: AsyncSession, key: str) -> Optional[Token]:
    stmt = (
        select(Token)
        .where(Token.key == key)
        .options(joinedload(Token.user, innerjoin=True))
    )
    result = await db.execute(stmt)
    return result.scalars().first()


async def get_or_create_token(db: AsyncSession, user: User) -> Tuple[Token, bool]:
    stmt = select(Token).where(Token.user_id == user.id)
    result = await db.execute(stmt)
    token = result.scalars().first()

    if token is not None:
        return token, False

    key = make_token_key()

    token = Token(key=key, user_id=user.id)

    db.add(token)
    await db.commit()
    await db.refresh(token)

    return token, True


async def delete_token(db: AsyncSession, token: Token) -> None:
    await db.delete(token)
    await db.commit()
