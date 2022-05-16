from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.types import ASGIApp
from xpresso import App

from server.config import Settings
from server.config.di import get_app_container, resolve

from .routes import routes

origins = [
    "http://localhost:3000",
]


def create_app() -> ASGIApp:
    settings = resolve(Settings)

    app = App(
        container=get_app_container(),
        routes=routes,
        docs_url=settings.docs_url,
        middleware=[
            Middleware(
                CORSMiddleware,
                allow_origins=origins,
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )
        ],
    )

    return app
