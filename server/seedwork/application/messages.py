from typing import TypeVar, Union

from .commands import Command
from .queries import Query

T = TypeVar("T")


class MessageBus:
    async def execute(self, message: Union[Command[T], Query[T]]) -> T:
        raise NotImplementedError
