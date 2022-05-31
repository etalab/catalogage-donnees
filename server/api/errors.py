from fastapi.encoders import jsonable_encoder
from pydantic import BaseConfig, ValidationError
from pydantic.error_wrappers import flatten_errors
from starlette.requests import Request
from starlette.responses import JSONResponse, Response


async def handle_validation_error(_: Request, exc: ValidationError) -> Response:
    """
    Handle validation errors that occurred beyond at the application layer, i.e.
    beyond basic data marshalling performed by schemas.
    """
    # Prepend 'body' in error locations, for consistency with API-level errors.
    errors = list(flatten_errors(exc.raw_errors, BaseConfig, loc=("body",)))

    return JSONResponse(
        status_code=422,
        content={"detail": jsonable_encoder(errors)},
    )


exception_handlers: dict = {
    ValidationError: handle_validation_error,
}
