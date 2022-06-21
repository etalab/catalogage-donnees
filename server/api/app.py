from debug_toolbar.middleware import DebugToolbarMiddleware
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware

from server.config import Settings
from server.config.di import resolve

from . import errors
from .auth.middleware import AuthMiddleware
from .resources import auth_backend
from .routes import router

origins = [
    "http://localhost:3000",
]


class App(FastAPI):
    def __init__(self, settings: Settings) -> None:
        super().__init__(
            debug=settings.debug,
            docs_url=settings.docs_url,
            exception_handlers=errors.exception_handlers,
            middleware=[
                Middleware(
                    CORSMiddleware,
                    allow_origins=origins,
                    allow_credentials=True,
                    allow_methods=["*"],
                    allow_headers=["*"],
                ),
                Middleware(AuthMiddleware, backend=auth_backend),
            ],
        )

        if settings.debug:
            self.add_middleware(
                DebugToolbarMiddleware,
                panels=["server.api.debugging.debug_toolbar.panels.SQLAlchemyPanel"],
            )

        self.include_router(router)

    def openapi(self) -> dict:
        # Tweak the OpenAPI schema.
        schema = super().openapi()
        schema.setdefault("components", {}).setdefault("securitySchemes", {}).update(
            auth_backend.get_openapi_security_definitions()
        )
        return schema


def create_app(settings: Settings = None) -> App:
    if settings is None:
        settings = resolve(Settings)

    return App(settings)
