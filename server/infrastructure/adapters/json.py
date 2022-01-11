import json
import uuid
from typing import Any


def _default(val: Any) -> str:
    if isinstance(val, uuid.UUID):
        return str(val)
    raise TypeError()


def dumps(d: Any) -> str:
    return json.dumps(d, default=_default)
