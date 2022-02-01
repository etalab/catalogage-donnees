import uuid
from typing import NewType

ID = NewType("ID", uuid.UUID)


def id_factory() -> ID:
    return ID(uuid.uuid4())
