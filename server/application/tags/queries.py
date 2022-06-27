from typing import List

from server.domain.common.types import ID
from server.seedwork.application.queries import Query

from .views import TagView


class GetAllTags(Query[List[TagView]]):
    pass


class GetTagByID(Query[TagView]):
    id: ID
