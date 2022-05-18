from types import SimpleNamespace
from typing import Callable, Generic, Iterator, TypeVar, Union

from pydantic.fields import ModelField

T = TypeVar("T")


class Computed(Generic[T]):
    """
    @property-like field for Pydantic, until Pydantic has this built-in.

    Usage:
        class Model(BaseModel):
            x: float
            x_squared: Computed[float] = Field(lambda self: self.x ** 2)

    Limitation: does not support re-computing when dependant fields such.

    Inspired by:
        https://github.com/samuelcolvin/pydantic/issues/935#issuecomment-961591416
    """

    validate_always = True

    @classmethod
    def __get_validators__(cls) -> Iterator:
        yield cls.validate

    @classmethod
    def validate(cls, v: Union[T, Callable], field: ModelField, values: dict) -> T:
        if not callable(v):
            return v

        assert field.sub_fields
        result = v(SimpleNamespace(**values))
        typ = field.sub_fields[0]
        validated, error = typ.validate(result, {}, loc="Expr")
        if error:
            raise ValueError(error)
        assert validated is not None
        return validated
