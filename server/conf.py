from pydantic import BaseSettings
from sqlalchemy.engine.url import make_url


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://localhost:5432/catalogage"
    testing: bool = False

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


settings = Settings()
