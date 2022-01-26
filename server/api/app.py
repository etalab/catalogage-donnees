from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from server.config import Settings
from server.config.di import resolve
from server.infrastructure.database import Database

from .routes import router


origins = [
    "http://localhost:3000",
]


def create_app() -> FastAPI:
    db = resolve(Database)
    settings = resolve(Settings)

    app = FastAPI(
        on_startup=[db.create_all],
        docs_url=settings.docs_url,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(router)

    return app
