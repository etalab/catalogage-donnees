from server.application.auth.views import AuthenticatedUserView, UserView
from server.config.di import resolve
from server.domain.auth.entities import User, UserRole
from server.domain.auth.exceptions import (
    EmailAlreadyExists,
    LoginFailed,
    UserDoesNotExist,
)
from server.domain.auth.repositories import UserRepository
from server.domain.common.types import ID

from .commands import ChangePassword, CreateUser, DeleteUser
from .passwords import PasswordEncoder, generate_api_token
from .queries import GetUserByAPIToken, GetUserByEmail, Login


async def create_user(
    command: CreateUser, *, id_: ID = None, role: UserRole = UserRole.USER
) -> ID:
    repository = resolve(UserRepository)
    password_encoder = resolve(PasswordEncoder)

    if id_ is None:
        id_ = repository.make_id()

    email = command.email

    user = await repository.get_by_email(email)

    if user is not None:
        raise EmailAlreadyExists(email)

    password_hash = password_encoder.hash(command.password)
    api_token = generate_api_token()

    user = User(
        id=id_,
        email=email,
        password_hash=password_hash,
        role=role,
        api_token=api_token,
    )

    return await repository.insert(user)


async def delete_user(command: DeleteUser) -> None:
    repository = resolve(UserRepository)
    await repository.delete(command.id)


async def login(query: Login) -> AuthenticatedUserView:
    repository = resolve(UserRepository)
    password_encoder = resolve(PasswordEncoder)

    user = await repository.get_by_email(query.email)

    if user is None:
        password_encoder.hash(query.password)  # Mitigate timing attacks.
        raise LoginFailed("Invalid credentials")

    if not password_encoder.verify(password=query.password, hash=user.password_hash):
        raise LoginFailed("Invalid credentials")

    return AuthenticatedUserView(**user.dict())


async def get_user_by_email(query: GetUserByEmail) -> UserView:
    repository = resolve(UserRepository)

    email = query.email

    user = await repository.get_by_email(email)

    if user is None:
        raise UserDoesNotExist(email)

    return UserView(**user.dict())


async def get_user_by_api_token(query: GetUserByAPIToken) -> UserView:
    repository = resolve(UserRepository)

    user = await repository.get_by_api_token(query.api_token)

    if user is None:
        raise UserDoesNotExist("__token__")

    return UserView(**user.dict())


async def change_password(command: ChangePassword) -> None:
    repository = resolve(UserRepository)
    password_encoder = resolve(PasswordEncoder)

    email = command.email
    user = await repository.get_by_email(email)

    if user is None:
        raise UserDoesNotExist(email)

    user.update_password(password_encoder.hash(command.password))
    user.update_api_token(generate_api_token())  # Require new login

    await repository.update(user)
