from server.config.di import resolve
from server.domain.auth.entities import User
from server.domain.auth.exceptions import (
    EmailAlreadyExists,
    LoginFailed,
    UserDoesNotExist,
)
from server.domain.auth.repositories import UserRepository
from server.domain.common.types import ID

from .commands import CreateUser, DeleteUser
from .passwords import PasswordEncoder, generate_api_token
from .queries import GetUserByAPIToken, GetUserByEmail, Login


async def create_user(command: CreateUser) -> ID:
    repository = resolve(UserRepository)
    password_encoder = resolve(PasswordEncoder)

    email = command.email

    user = await repository.get_by_email(email)

    if user is not None:
        raise EmailAlreadyExists(email)

    password_hash = password_encoder.hash(command.password)
    api_token = generate_api_token()

    user = User(
        id=repository.make_id(),
        email=email,
        password_hash=password_hash,
        api_token=api_token,
    )

    return await repository.insert(user)


async def delete_user(command: DeleteUser) -> None:
    repository = resolve(UserRepository)
    await repository.delete(command.id)


async def login(query: Login) -> User:
    repository = resolve(UserRepository)
    password_encoder = resolve(PasswordEncoder)

    email = query.email

    user = await repository.get_by_email(email)

    if user is None:
        password_encoder.hash(query.password)  # Mitigate timing attacks.
        raise LoginFailed("Invalid credentials")

    if not password_encoder.verify(password=query.password, hash=user.password_hash):
        raise LoginFailed("Invalid credentials")

    return user


async def get_user_by_email(query: GetUserByEmail) -> User:
    repository = resolve(UserRepository)

    email = query.email

    user = await repository.get_by_email(email)

    if user is None:
        raise UserDoesNotExist(email)

    return user


async def get_user_by_api_token(query: GetUserByAPIToken) -> User:
    repository = resolve(UserRepository)

    user = await repository.get_by_api_token(query.api_token)

    if user is None:
        raise UserDoesNotExist("__token__")

    return user
