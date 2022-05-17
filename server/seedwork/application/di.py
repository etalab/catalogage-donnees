from typing import Callable, Optional, Type, TypeVar

import punq

T = TypeVar("T")


class Container:
    """
    Implements a configurable DI container.
    """

    def __init__(
        self, configure: Callable[["Container"], None] = lambda _: None
    ) -> None:
        self._impl: Optional[punq.Container] = None
        self._configure = configure

    def bootstrap(self) -> None:
        self._impl = punq.Container()
        self._configure(self)

    def register_instance(self, type_: Type[T], instance: T) -> None:
        """
        Register a singleton instance.
        """
        assert self._impl is not None
        self._impl.register(type_, instance=instance)

    def resolve(self, type_: Type[T]) -> T:
        if self._impl is None:
            raise RuntimeError("Container not ready. Please call bootstrap()")

        try:
            return self._impl.resolve(type_)
        except punq.MissingDependencyError:
            raise RuntimeError(f"Failed to resolve implementation for {type_}")
