from server.application.tags.commands import CreateTag
from server.application.tags.handlers import create_tag, get_tag_by_id
from server.application.tags.queries import GetTagByID
from server.seedwork.application.modules import Module


class TagsModule(Module):
    command_handlers = {
        CreateTag: create_tag,
    }

    query_handlers: dict = {
        GetTagByID: get_tag_by_id,
    }
