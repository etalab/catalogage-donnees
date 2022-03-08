from typing import Any, TypeVar, Union

from .commands import Command
from .queries import Query

T = TypeVar("T")


class MessageBus:
    async def execute(self, message: Union[Command[T], Query[T]], **kwargs: Any) -> T:
        raise NotImplementedError
