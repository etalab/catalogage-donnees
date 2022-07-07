import importlib
from typing import ClassVar, List

from .types import CommandHandlers, QueryHandlers


class Module:
    command_handlers: ClassVar[CommandHandlers] = {}
    query_handlers: ClassVar[QueryHandlers] = {}


def load_modules(paths: List[str]) -> List[Module]:
    """
    Load modules by Python path.

    server.application.example.module.ExampleModule -> ExampleModule
    """
    modules = []
    for classpath in paths:
        modpath, _, classname = classpath.rpartition(".")
        mod = importlib.import_module(modpath)
        modules.append(getattr(mod, classname))
    return modules
