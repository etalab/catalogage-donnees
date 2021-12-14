from fastapi import FastAPI

from . import events
from .routes import router


def create_app() -> FastAPI:
    app = FastAPI(on_startup=events.startup)

    app.include_router(router)

    return app
