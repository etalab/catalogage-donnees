from fastapi import FastAPI

from . import events
from .conf import settings
from .routes import router


def create_app() -> FastAPI:
    app = FastAPI(on_startup=events.startup, docs_url=settings.docs_url)

    app.include_router(router)

    return app
