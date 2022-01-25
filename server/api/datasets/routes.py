import falcon
import falcon.asgi
import falcon.routing

from server.application.datasets.commands import CreateDataset, DeleteDataset
from server.application.datasets.queries import GetAllDatasets, GetDatasetByID
from server.config.di import resolve
from server.domain.common.types import ID
from server.domain.datasets.exceptions import DatasetDoesNotExist
from server.seedwork.application.messages import MessageBus

from .schemas import DatasetCreate, DatasetRead


class DatasetList:
    async def on_get(
        self, req: falcon.asgi.Request, resp: falcon.asgi.Response
    ) -> None:
        bus = resolve(MessageBus)
        query = GetAllDatasets()
        datasets = await bus.execute(query)

        resp.status = falcon.HTTP_200
        resp.media = [DatasetRead(**dataset.dict()).dict() for dataset in datasets]

    async def on_post(
        self, req: falcon.asgi.Request, resp: falcon.asgi.Response
    ) -> None:
        data = DatasetCreate(**(await req.get_media()))

        bus = resolve(MessageBus)
        command = CreateDataset(name=data.name)
        pk = await bus.execute(command)

        query = GetDatasetByID(id=pk)
        dataset = await bus.execute(query)

        resp.status = falcon.HTTP_201
        resp.media = DatasetRead(**dataset.dict()).dict()


class DatasetDetail:
    async def on_get(
        self, req: falcon.asgi.Request, resp: falcon.asgi.Response, *, pk: ID
    ) -> None:
        bus = resolve(MessageBus)

        query = GetDatasetByID(id=pk)
        try:
            dataset = await bus.execute(query)
        except DatasetDoesNotExist:
            raise falcon.HTTPError(404)

        resp.status = falcon.HTTP_200
        resp.media = DatasetRead(**dataset.dict()).dict()

    async def on_delete(
        self, req: falcon.asgi.Request, resp: falcon.asgi.Response, *, pk: ID
    ) -> None:
        bus = resolve(MessageBus)

        command = DeleteDataset(id=pk)
        await bus.execute(command)

        resp.status = falcon.HTTP_204


async def handle_http_error(
    req: falcon.asgi.Request,
    resp: falcon.asgi.Response,
    exc: falcon.HTTPError,
    params: dict,
) -> None:
    resp.status = getattr(falcon, f"HTTP_{exc.status}")
    resp.media = exc.to_dict()


app = falcon.asgi.App()
app.add_route("/", DatasetList())
app.add_route("/{pk}/", DatasetDetail())
app.add_error_handler(falcon.HTTPError, handle_http_error)
