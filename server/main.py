from .api.app import create_app
from .config.di import bootstrap

bootstrap()

app = create_app()

if __name__ == "__main__":
    import uvicorn

    from .config.di import resolve
    from .config.settings import Settings

    settings = resolve(Settings)

    kwargs: dict = {
        "host": "127.0.0.1",
        "port": 3579,
    }

    if settings.debug:
        kwargs.update(
            # Enable hot reload in development.
            reload=True,
            reload_dirs=["server"],
        )
    else:
        kwargs.update(
            # Pass any proxy headers, so that Uvicorn sees information about the
            # connecting client, rather than the connecting Nginx proxy.
            # See: https://www.uvicorn.org/deployment/#running-behind-nginx
            proxy_headers=True,
            # Match Nginx mount path.
            root_path="/api",
        )

    uvicorn.run("server.main:app", **kwargs)
