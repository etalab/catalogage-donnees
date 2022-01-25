from fastapi import FastAPI

from server.config import Settings
from server.config.di import resolve
from server.infrastructure.database import Database

from . import datasets
from .routes import router


def create_app() -> FastAPI:
    db = resolve(Database)
    settings = resolve(Settings)

    app = FastAPI(
        on_startup=[db.create_all],
        docs_url=settings.docs_url,
    )

    app.include_router(router)
    app.mount("/datasets/", datasets.app)

    return app
