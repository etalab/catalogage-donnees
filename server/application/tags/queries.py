from typing import List

from server.domain.common.types import ID
from server.domain.tags.entities import Tag
from server.seedwork.application.queries import Query


class GetAllTags(Query[List[Tag]]):
    pass


class GetTagByID(Query[Tag]):
    id: ID
