from typing import Awaitable, Callable, Dict, Type, TypeVar, Union

from server.seedwork.application.commands import Command
from server.seedwork.application.messages import MessageBus
from server.seedwork.application.queries import Query

T = TypeVar("T")
F = TypeVar("F", bound=Callable[..., Awaitable])


class MessageBusAdapter(MessageBus):
    def __init__(
        self,
        command_handlers: Dict[Type[Command], Callable[..., Awaitable]],
        query_handlers: Dict[Type[Query], Callable[..., Awaitable]],
    ) -> None:
        self.command_handlers = command_handlers
        self.query_handlers = query_handlers

    async def execute(self, message: Union[Command[T], Query[T]]) -> T:
        try:
            if isinstance(message, Command):
                handler = self.command_handlers[type(message)]
            else:
                handler = self.query_handlers[type(message)]
        except KeyError:
            raise NotImplementedError(f"No handler for {type(message)}")

        return await handler(message)
