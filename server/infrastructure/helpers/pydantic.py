import math
from typing import Generic, Iterator, TypeVar, Union

from pydantic.fields import ModelField

T = TypeVar("T")


class Computed(Generic[T]):
    """
    @property-like field for Pydantic, until Pydantic has this built-in.

    Usage:
        class Model(BaseModel):
            x: float
            x_squared: Computed[float] = Field("lambda self: self.x ** 2")

    Limitation: does not support re-computing when dependant fields such.

    Inspired by:
        https://github.com/samuelcolvin/pydantic/issues/935#issuecomment-961591416
    """

    class Expr(str):
        pass

    __expr_globals__ = {"math": math}

    validate_always = True

    @classmethod
    def __get_validators__(cls) -> Iterator:
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema: dict, field: ModelField) -> None:
        field_schema["default"] = f"Computed({field.default})"

    @classmethod
    def validate(cls, v: Union[T, Expr], field: ModelField, values: dict) -> T:
        if not isinstance(v, cls.Expr):
            return v

        assert field.sub_fields
        result = eval(v, cls.__expr_globals__, values)
        typ = field.sub_fields[0]
        validated, error = typ.validate(result, {}, loc="Computed")
        if error:
            raise ValueError(error)
        assert validated is not None
        return validated
