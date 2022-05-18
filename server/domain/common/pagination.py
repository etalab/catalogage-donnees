import math
from typing import Generic, List, TypeVar

from pydantic import BaseModel, Field
from pydantic.generics import GenericModel
from typing_extensions import Annotated

from server.infrastructure.helpers.pydantic import Computed

T = TypeVar("T")

PAGE_NUMBER_CONSTR: dict = {"ge": 1, "le": 10_000}
PAGE_SIZE_CONSTR: dict = {"ge": 1, "le": 100}

PageNumber = Annotated[int, Field(**PAGE_NUMBER_CONSTR)]
PageSize = Annotated[int, Field(**PAGE_SIZE_CONSTR)]


class Page(BaseModel):
    number: PageNumber = 1
    size: PageSize = 10

    class Config:
        allow_mutation = False


class Pagination(GenericModel, Generic[T]):
    items: List[T]
    total_items: int
    page_size: int
    total_pages: Computed[int] = Field(
        lambda self: math.ceil(self.total_items / self.page_size)
    )

    class Config:
        allow_mutation = False
