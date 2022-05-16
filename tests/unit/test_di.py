from dataclasses import dataclass

import pytest

from server.seedwork.application.di import Container


@dataclass
class Person:
    name: str


def test_container_empty() -> None:
    container = Container()

    with pytest.raises(RuntimeError, match="Container not ready"):
        container.resolve(Person)

    container.bootstrap()

    with pytest.raises(RuntimeError, match="Failed to resolve implementation"):
        container.resolve(Person)


def test_container_configured() -> None:
    @dataclass
    class Person:
        name: str

    def configure(container: Container) -> None:
        container.register_instance(Person, Person("Tiffany"))

    container = Container(configure)
    container.bootstrap()
    person = container.resolve(Person)
    assert person.name == "Tiffany"
