from fastapi import FastAPI

from .routes import router


def create_app() -> FastAPI:
    app = FastAPI()

    app.include_router(router)

    return app
