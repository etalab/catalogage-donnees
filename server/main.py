from .api.app import create_app
from .config.di import bootstrap, resolve
from .config.settings import Settings

bootstrap()

app = create_app()

if __name__ == "__main__":
    import uvicorn

    settings = resolve(Settings)

    args = ["server.main:app"]

    kwargs: dict = {
        "port": 3579,
    }

    if settings.debug:
        kwargs.update(
            # Enable hot reload during development.
            reload=True,
            reload_dir=["server"],
        )
    else:
        kwargs.update(
            # Production is served behind Nginx.
            # Pass proxy headers so Uvicorn properly reads e.g. any mounted root path.
            # See: https://www.uvicorn.org/deployment/#running-behind-nginx
            proxy_headers=True
        )

    uvicorn.run(*args, **kwargs)
