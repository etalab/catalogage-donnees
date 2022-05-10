from typing import Generic, List, TypeVar

from pydantic import BaseModel, Field
from pydantic.generics import GenericModel
from typing_extensions import Annotated

T = TypeVar("T")

# TODO: set this back to 10 when implementing pagination in the frontend
TEMP_VERY_HIGH_MAX_PAGE_SIZE = 1000

PAGE_NUMBER_CONSTR: dict = {"ge": 1, "le": 10_000}
PAGE_SIZE_CONSTR: dict = {"ge": 1, "le": TEMP_VERY_HIGH_MAX_PAGE_SIZE}

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
