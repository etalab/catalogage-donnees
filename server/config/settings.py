from typing import Literal, Optional

from pydantic import BaseSettings, SecretStr
from sqlalchemy.engine.url import make_url

ServerMode = Literal["local", "live"]


class Settings(BaseSettings):
    # For usage, see: https://pydantic-docs.helpmanual.io/usage/settings/

    server_mode: ServerMode = "local"
    database_url: str = "postgresql+asyncpg://localhost:5432/catalogage"
    host: str = "localhost"
    port: int = 3579
    docs_url: str = "/docs"

    debug: bool = False
    testing: bool = False

    # Emails
    email_backend: str = (
        "server.infrastructure.emails.backends.console.ConsoleEmailBackend"
    )
    mailpace_api_token: Optional[SecretStr] = None

    class Config:
        env_prefix = "app_"
        env_file = ".env"

    @property
    def test_database_url(self) -> str:
        url = make_url(self.database_url)
        url = url.set(database=f"{url.database}-test")
        return str(url)

    @property
    def sync_test_database_url(self) -> str:
        url = make_url(self.test_database_url)
        url = url.set(
            drivername="postgresql",  # Test database setup uses sync engine
        )
        return str(url)

    @property
    def env_database_url(self) -> str:
        return self.test_database_url if self.testing else self.database_url
