from typing import Any


class _NetworkForbidden(Exception):
    pass


def socket_connect_fail(*args: Any, **kwargs: Any) -> Any:
    raise _NetworkForbidden()
