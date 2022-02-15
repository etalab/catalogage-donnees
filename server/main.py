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
        "port": settings.port,
    }

    if settings.server_mode == "local":
        kwargs.update(
            # Enable hot reload.
            reload=True,
            reload_dirs=["server"],
        )
    elif settings.server_mode == "live":
        kwargs.update(
            # Pass any proxy headers, so that Uvicorn sees information about the
            # connecting client, rather than the connecting Nginx proxy.
            # See: https://www.uvicorn.org/deployment/#running-behind-nginx
            proxy_headers=True,
        )

    uvicorn.run("server.main:app", **kwargs)
