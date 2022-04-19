from server.application.tags.queries import GetTagByID
from server.config.di import resolve
from server.domain.common.types import ID
from server.domain.tags.entities import Tag
from server.domain.tags.exceptions import TagDoesNotExist
from server.domain.tags.repositories import TagRepository

from .commands import CreateTag


async def create_tag(command: CreateTag, *, id_: ID = None) -> ID:
    repository = resolve(TagRepository)

    if id_ is None:
        id_ = repository.make_id()

    tag = Tag(id=id_, **command.dict())

    return await repository.insert(tag)


async def get_tag_by_id(query: GetTagByID) -> Tag:
    repository = resolve(TagRepository)

    id_ = query.id
    tag = await repository.get_by_id(id_)

    if tag is None:
        raise TagDoesNotExist(id_)

    return tag
