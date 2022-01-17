from typing import Awaitable, Callable, Dict, Type

from .commands import Command
from .queries import Query

CommandHandlers = Dict[Type[Command], Callable[..., Awaitable]]

QueryHandlers = Dict[Type[Query], Callable[..., Awaitable]]
