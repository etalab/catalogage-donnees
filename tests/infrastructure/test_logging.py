import json
import logging

import pytest

from server.config.di import configure
from server.config.settings import Settings
from server.infrastructure.server import get_server_config
from server.seedwork.application.di import Container


def test_logging(capsys: pytest.CaptureFixture) -> None:
    config = get_server_config("server.main:app")
    config.load()

    logger = logging.getLogger("server.example")
    logger.debug("Debug test")
    logger.info("Info test")

    captured = capsys.readouterr()
    assert not captured.err
    assert "Debug test" not in captured.out
    assert "server.example: Info test" in captured.out


def test_logging_debug(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture
) -> None:
    monkeypatch.setenv("APP_DEBUG", "1")

    container = Container(configure)
    container.bootstrap()

    settings = container.resolve(Settings)
    config = get_server_config("server.main:app", settings)
    config.load()

    logger = logging.getLogger("server.example")
    logger.debug("Debug test")

    captured = capsys.readouterr()
    assert not captured.err
    assert "server.example: Debug test" in captured.out


def test_logging_live_renders_json(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture
) -> None:
    monkeypatch.setenv("APP_SERVER_MODE", "live")

    container = Container(configure)
    container.bootstrap()

    settings = container.resolve(Settings)
    config = get_server_config("server.main:app", settings)
    config.load()

    logger = logging.getLogger("server.example")
    logger.info("Info test")

    captured = capsys.readouterr()
    assert not captured.err
    info_line = json.loads(
        next(line for line in captured.out.splitlines() if "Info test" in line)
    )
    assert info_line == {
        "asctime": info_line["asctime"],
        "levelname": "INFO",
        "name": "server.example",
        "message": "Info test",
    }
