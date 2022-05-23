from debug_toolbar.panels.sqlalchemy import SQLAlchemyPanel as Base
from fastapi import Request, Response
from fastapi.encoders import jsonable_encoder

from server.config.di import resolve
from server.infrastructure.database import Database


class SQLAlchemyPanel(Base):
    def after_execute(self, *args) -> None:  # type: ignore
        # HACK: base SQL panel calls json.dumps(parameters) at some point.
        # Ensure values such as UUIDs can be dumped.
        parameters = args[3]
        args = (*args[:3], jsonable_encoder(parameters), *args[4:])
        return super().after_execute(*args)

    async def process_request(self, request: Request) -> Response:
        db = resolve(Database)
        engine = db.engine.sync_engine

        self.register(engine)
        try:
            return await super().process_request(request)
        finally:
            self.unregister(engine)
