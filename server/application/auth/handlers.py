from server.config.di import resolve
from server.domain.auth.entities import User
from server.domain.auth.exceptions import EmailAlreadyExists, UserDoesNotExist
from server.domain.auth.repositories import UserRepository
from server.domain.common.types import ID

from .commands import CreateUser, DeleteUser
from .queries import GetUserByEmail


async def create_user(command: CreateUser) -> ID:
    repository = resolve(UserRepository)

    email = command.email

    user = await repository.get_by_email(email)

    if user is not None:
        raise EmailAlreadyExists(email)

    user = User(id=repository.make_id(), email=email)
    return await repository.insert(user)


async def delete_user(command: DeleteUser) -> None:
    repository = resolve(UserRepository)
    await repository.delete(command.id)


async def get_user_by_email(query: GetUserByEmail) -> User:
    repository = resolve(UserRepository)

    email = query.email

    user = await repository.get_by_email(email)

    if user is None:
        raise UserDoesNotExist(email)

    return user
