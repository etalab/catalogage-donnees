from debug_toolbar.middleware import DebugToolbarMiddleware
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

    app = App(
        debug=settings.debug,
        docs_url=settings.docs_url,
        exception_handlers=errors.exception_handlers,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_middleware(AuthMiddleware, backend=auth_backend)

    if settings.debug:
        app.add_middleware(
            DebugToolbarMiddleware,
            panels=["server.api.debugging.debug_toolbar.panels.SQLAlchemyPanel"],
        )

    app.include_router(router)

    return app
