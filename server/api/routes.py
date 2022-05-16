from starlette.datastructures import URLPath
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.routing import Mount
from xpresso import Operation, Path

from server.config import Settings
from server.config.di import resolve

from . import auth, datasets, tags


def index(request: Request) -> str:
    settings = resolve(Settings)
    return URLPath(settings.docs_url).make_absolute_url(request.base_url)


routes = [
    Path(
        "/",
        get=Operation(
            index, response_factory=RedirectResponse, include_in_schema=False
        ),
    ),
    Mount("/auth", routes=auth.routes),
    Mount("/datasets", routes=datasets.routes),
    Mount("/tags", routes=tags.routes),
]
