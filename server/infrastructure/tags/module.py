from server.application.tags.commands import CreateTag
from server.application.tags.handlers import create_tag, get_all_tags, get_tag_by_id
from server.application.tags.queries import GetAllTags, GetTagByID
from server.seedwork.application.modules import Module


class TagsModule(Module):
    command_handlers = {
        CreateTag: create_tag,
    }

    query_handlers: dict = {
        GetAllTags: get_all_tags,
        GetTagByID: get_tag_by_id,
    }
