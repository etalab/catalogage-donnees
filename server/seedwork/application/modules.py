from typing import ClassVar

from .types import CommandHandlers, QueryHandlers


class Module:
    command_handlers: ClassVar[CommandHandlers]
    query_handlers: ClassVar[QueryHandlers]
