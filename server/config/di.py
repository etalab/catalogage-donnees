"""
Dependency injection (DI) setup.

Allows decoupling interfaces used by the application from their
concrete implementation, which might be configured on init.

Uses: https://punq.readthedocs.io/

Usage
-----

The DI container should first be initialized in entrypoints:

    ```python
    from server.config.di import bootstrap

    def main():
        bootstrap()
        ...
    ```

Then, register dependencies in `create_container` below:

    ```python
    from server.domain.todos.repositories import TodoRepository
    from server.infrastructure.todos.repositories import SqlTodoRepository

    container.register(TodoRepository, SqlTodoRepository)
    ```

Then, you can resolve dependencies elsewhere in the project,
e.g. in command or query handlers:

    ```python
    # server/application/todos/handlers.py
    from server.config.di import resolve
    from server.domain.todos.repositories import TodoRepository

    from .commands import CreateTodo

    async def create_todo(command: CreateTodo):
        repository = resolve(TodoRepository)
        ...
    ```

Or in FastAPI routes:

    ```python
    # server/api/todos/routes.py
    from server.config.di import resolve
    from server.seedwork.application.messages import MessageBus
    from server.application.todos.commands import CreateTodo

    ...

    @router.get(...)
    async def create_todo(...):
        bus = resolve(MessageBus)
        command = CreateTodo(...)
        todo = await bus.execute(command)
        ...
    ```
"""
import contextlib
import importlib
from typing import Iterator, List, Type, TypeVar

import punq

from server.application.auth.passwords import PasswordEncoder
from server.domain.auth.repositories import UserRepository
from server.domain.catalog_records.repositories import CatalogRecordRepository
from server.domain.datasets.repositories import DatasetRepository
from server.infrastructure.adapters.messages import MessageBusAdapter
from server.infrastructure.auth.passwords import Argon2PasswordEncoder
from server.infrastructure.auth.repositories import SqlUserRepository
from server.infrastructure.catalog_records.repositories import (
    SqlCatalogRecordRepository,
)
from server.infrastructure.database import Database
from server.infrastructure.datasets.repositories import SqlDatasetRepository
from server.seedwork.application.messages import MessageBus
from server.seedwork.application.modules import Module

from .settings import Settings

T = TypeVar("T")


# Edit this as appropriate to register modules of command and query handlers.
# They are imported lazily later on, to avoid circular dependencies.
MODULES = [
    "server.infrastructure.datasets.module.DatasetsModule",
    "server.infrastructure.auth.module.AuthModule",
]


def get_modules() -> List[Module]:
    modules = []
    for classpath in MODULES:
        modpath, _, classname = classpath.rpartition(".")
        mod = importlib.import_module(modpath)
        modules.append(getattr(mod, classname))
    return modules


def create_container() -> punq.Container:
    """
    Configure the Dependency Injection (DI) container.

    NOTE: Edit this as appropriate to register dependencies.
    """
    container = punq.Container()

    # Application-wide configuration

    settings = Settings()
    container.register(Settings, instance=settings)

    # Common services

    container.register(PasswordEncoder, instance=Argon2PasswordEncoder())

    # Event handling (Commands, queries, and the message bus)

    modules = get_modules()

    command_handlers = {
        command: handler
        for cls in modules
        for command, handler in cls.command_handlers.items()
    }

    query_handlers = {
        query: handler
        for cls in modules
        for query, handler in cls.query_handlers.items()
    }

    bus = MessageBusAdapter(command_handlers, query_handlers)

    container.register(MessageBus, instance=bus)

    # Databases

    container.register(
        Database,
        instance=Database(url=settings.env_database_url, debug=settings.sql_debug),
    )

    # Repositories

    container.register(UserRepository, SqlUserRepository)
    container.register(CatalogRecordRepository, SqlCatalogRecordRepository)
    container.register(DatasetRepository, SqlDatasetRepository)

    return container


_CONTAINER_STACK: List[punq.Container] = []


def bootstrap() -> None:
    _CONTAINER_STACK.clear()
    _CONTAINER_STACK.append(create_container())


def resolve(type: Type[T]) -> T:
    return _CONTAINER_STACK[-1].resolve(type)


@contextlib.contextmanager
def override() -> Iterator[punq.Container]:
    """
    Override certain dependencies on the DI container, e.g. for testing purposes.
    """
    container = create_container()
    _CONTAINER_STACK.append(container)
    try:
        yield container
    finally:
        _CONTAINER_STACK.pop(0)
