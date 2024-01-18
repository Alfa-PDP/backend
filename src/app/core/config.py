from pydantic import Field
from pydantic_settings import BaseSettings


class RedisConfig(BaseSettings):
    port: int = Field(default=6379, alias="redis_port")
    host: str = Field(default="127.0.0.1", alias="redis_host")


class ProjectConfig(BaseSettings):
    name: str = Field(default="dpd_api", alias="PROJECT_NAME")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    api_prefix: str = Field(default="/api")
    docs_url: str = Field(default="/openapi")
    openapi_url: str = Field(default="/api/openapi.json")
    description: str = Field(default="Alfa-Bank PDP")
    version: str = Field(default="0.1.0")


class PostgresqlConfig(BaseSettings):
    db: str = Field(default=..., alias="postgres_db")
    user: str = Field(default=..., alias="postgres_user")
    password: str = Field(default=..., alias="postgres_password")
    host: str = Field(default=..., alias="postgres_host")
    port: str = Field(default=..., alias="postgres_port")
    echo: bool = Field(default=False, alias="sqlalchemy_echo")

    @property
    def database_url(self) -> str:
        """Получить ссылку для подключения к DB."""
        return f"postgresql+asyncpg://" f"{self.user}:{self.password}" f"@{self.host}:{self.port}/{self.db}"


class MainConfig(BaseSettings):
    project: ProjectConfig = ProjectConfig()
    redis: RedisConfig = RedisConfig()
    postgresql: PostgresqlConfig = PostgresqlConfig()
