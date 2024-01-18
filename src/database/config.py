import os
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent

ENV_FILE = str(BASE_DIR / ".env")
ENV_FILE_LOCAL = str(BASE_DIR / ".env.local")


class PostgresqlConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=(ENV_FILE, ENV_FILE_LOCAL), extra="allow")

    db: str = Field(default=..., alias="postgres_db")
    user: str = Field(default=..., alias="postgres_user")
    password: str = Field(default=..., alias="postgres_password")
    host: str = Field(default=..., alias="postgres_host")
    port: str = Field(default=..., alias="postgres_port")

    @property
    def database_url(self) -> str:
        """Получить ссылку для подключения к DB."""
        return f"postgresql+asyncpg://" f"{self.user}:{self.password}" f"@{self.host}:{self.port}/{self.db}"
