from contextlib import contextmanager
from typing import Iterator, List, Sequence, Tuple

from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from pydantic.error_wrappers import ErrorList, ErrorWrapper


@contextmanager
def wrap_request_validation_errors() -> Iterator[None]:
    try:
        yield
    except ValidationError as exc:
        errors = _add_loc_prefix(exc.raw_errors, ("body",))
        raise RequestValidationError([errors])


def _add_loc_prefix(
    raw_errors: Sequence[ErrorList], prefix: Tuple[str, ...]
) -> List[ErrorWrapper]:
    errors: List[ErrorWrapper] = []

    for raw_error in raw_errors:
        if isinstance(raw_error, ErrorWrapper):
            errors.append(
                ErrorWrapper(raw_error.exc, loc=(*prefix, *raw_error.loc_tuple()))
            )
        else:
            assert isinstance(raw_error, list)
            errors.extend(_add_loc_prefix(raw_error, prefix))

    return errors
