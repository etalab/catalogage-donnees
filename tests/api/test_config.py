from server.config import Settings
from server.config.di import resolve
from server.infrastructure.server import get_server_config


def test_server_config_local() -> None:
    settings = resolve(Settings).copy(update={"server_mode": "local"})

    config = get_server_config("server.main:app", settings)

    assert config.host == "localhost"
    assert config.port == 3579
    assert config.should_reload
    assert config.root_path == ""


def test_server_config_live() -> None:
    settings = resolve(Settings).copy(update={"server_mode": "live"})

    config = get_server_config("server.main:app", settings)

    assert config.host == "localhost"
    assert config.port == 3579
    assert config.proxy_headers
    assert config.root_path == "/api"
