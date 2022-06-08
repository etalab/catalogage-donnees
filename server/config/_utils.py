import importlib
from typing import Any


def load_object(path: str) -> Any:
    modpath, _, objname = path.rpartition(".")
    mod = importlib.import_module(modpath)
    return getattr(mod, objname)
