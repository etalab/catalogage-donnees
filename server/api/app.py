from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from server.config import Settings
from server.config.di import resolve

from .routes import router

origins = [
    "http://localhost:3000",
]


def create_app() -> FastAPI:
    settings = resolve(Settings)

    app = FastAPI(
        docs_url=settings.docs_url,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
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
