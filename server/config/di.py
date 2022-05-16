"""
Dependency injection (DI) setup.

Allows decoupling interfaces used by the application from their
concrete implementation, which might be configured on init.

Uses: https://www.adriangb.com/di/

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

    register(TodoRepository, SqlTodoRepository)
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

Or in routes:

    ```python
    # server/api/todos/routes.py
    from server.config.di import resolve
    from server.seedwork.application.messages import MessageBus
    from server.application.todos.commands import CreateTodo

    ...

    async def create_todo(...):
        bus = resolve(MessageBus)
        command = CreateTodo(...)
        todo = await bus.execute(command)
        ...
    ```
"""
import contextlib
import functools
import importlib
from typing import Any, List, Optional, Type, TypeVar, cast

from di.api.providers import CallableProvider
from di.container import Container as ContainerImpl
from di.container import ContainerState, bind_by_type
from di.dependant import Dependant
from di.executors import SyncExecutor

from server.application.auth.passwords import PasswordEncoder
from server.domain.auth.repositories import UserRepository
from server.domain.catalog_records.repositories import CatalogRecordRepository
from server.domain.datasets.repositories import DatasetRepository
from server.domain.tags.repositories import TagRepository
from server.infrastructure.adapters.messages import MessageBusAdapter
from server.infrastructure.auth.passwords import Argon2PasswordEncoder
from server.infrastructure.auth.repositories import SqlUserRepository
from server.infrastructure.catalog_records.repositories import (
    SqlCatalogRecordRepository,
)
from server.infrastructure.database import Database
from server.infrastructure.datasets.repositories import SqlDatasetRepository
from server.infrastructure.tags.repositories import SqlTagRepository
from server.seedwork.application.messages import MessageBus
from server.seedwork.application.modules import Module

from .settings import Settings

T = TypeVar("T")


# Edit this as appropriate to register modules of command and query handlers.
# They are imported lazily later on, to avoid circular dependencies.
MODULES = [
    "server.infrastructure.datasets.module.DatasetsModule",
    "server.infrastructure.tags.module.TagsModule",
    "server.infrastructure.auth.module.AuthModule",
]


def get_modules() -> List[Module]:
    modules = []
    for classpath in MODULES:
        modpath, _, classname = classpath.rpartition(".")
        mod = importlib.import_module(modpath)
        modules.append(getattr(mod, classname))
    return modules


def _create_container() -> ContainerImpl:
    """
    Configure the Dependency Injection (DI) container.

    NOTE: Edit this as appropriate to register dependencies.
    """
    container = ContainerImpl()

    def register_instance(dependency: Type[T], instance: T) -> None:
        container.bind(
            bind_by_type(Dependant(lambda: instance, scope="global"), dependency)
        )

    # Application-wide configuration

    settings = Settings()
    register_instance(Settings, settings)

    # Common services

    register_instance(PasswordEncoder, Argon2PasswordEncoder())

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
    register_instance(MessageBus, bus)

    # Databases

    db = Database(url=settings.env_database_url, debug=settings.sql_debug)
    register_instance(Database, db)

    # Repositories

    register_instance(UserRepository, SqlUserRepository(db))
    register_instance(CatalogRecordRepository, SqlCatalogRecordRepository(db))
    register_instance(DatasetRepository, SqlDatasetRepository(db))
    register_instance(TagRepository, SqlTagRepository(db))

    return container


class Container:
    def __init__(self) -> None:
        self._impl: Optional[ContainerImpl] = None
        self._executor = SyncExecutor()
        self._stack = contextlib.ExitStack()
        self._state: Optional[ContainerState] = None

    def get_impl(self) -> ContainerImpl:
        if self._impl is None:
            raise RuntimeError("Container not ready. Please call bootstrap()")
        return self._impl

    def bootstrap(self) -> None:
        self._impl = _create_container()
        self._state = self._stack.enter_context(self._impl.enter_scope("global"))

    def resolve(self, type_: Type[T]) -> T:
        container = self.get_impl()
        assert self._state is not None
        solved = container.solve(Dependant(type_, scope="global"), scopes=["global"])
        return container.execute_sync(
            solved, executor=self._executor, state=self._state
        )


_CONTAINER = Container()

get_app_container = _CONTAINER.get_impl
bootstrap = _CONTAINER.bootstrap
resolve = _CONTAINER.resolve
