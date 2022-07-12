from typing import Any, Callable, Iterator, Union


class Siret(str):
    # This is a custom Pydantic field type.
    # See: https://pydantic-docs.helpmanual.io/usage/types/#custom-data-types

    def __new__(cls, value: Union[str, "Siret"]) -> "Siret":
        if not isinstance(value, Siret):
            value = cls.validate(value)
        return super().__new__(cls, value)

    @classmethod
    def __get_validators__(cls) -> Iterator[Callable]:
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema: dict) -> None:
        field_schema.update(
            format="siret",
            examples=["011 605 754 00330", "77908899900227"],
        )

    @classmethod
    def validate(cls, v: Any) -> str:
        # Perform basic format validation: a string of 14 digits.
        # The full SIRET format has a control number and various exceptions:
        # https://www.insee.fr/fr/metadonnees/definition/c1841
        # But we assume manual verification of the SIRET number will be done
        # upon creation by knowledgeable administrators.

        if not isinstance(v, str):
            raise TypeError("string required")

        # Ignore spaces.
        v = v.replace(" ", "")

        if not v.isdigit():
            raise ValueError("must contain digits only")

        if len(v) != 14:
            raise ValueError("must contain exactly 14 digits")

        return v
