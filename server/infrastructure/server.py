from typing import Callable, Union

import uvicorn
import uvicorn.supervisors

from server.config.di import resolve
from server.config.settings import Settings

from .logging.config import get_log_config


def get_server_config(
    app: Union[str, Callable], settings: Settings = None
) -> uvicorn.Config:
    if settings is None:
        settings = resolve(Settings)

    kwargs = dict(
        host=settings.host,
        port=settings.port,
        log_config=get_log_config(settings),
    )

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
            # Match Nginx mount path.
            root_path="/api",
        )

    return uvicorn.Config(app, **kwargs)


class Server(uvicorn.Server):
    pass


def run(app: Union[str, Callable]) -> int:
    """
    Run the API server.

    This is a simplified version of `uvicorn.run()`.
    """
    config = get_server_config(app)
    server = Server(config)

    if config.should_reload:
        sock = config.bind_socket()
        reloader = uvicorn.supervisors.ChangeReload(
            config, target=server.run, sockets=[sock]
        )
        reloader.run()
        return 0

    server.run()

    if not server.started:
        return 3

    return 0
