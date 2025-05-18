from pydantic import BaseModel, PostgresDsn, field_validator

from loguru import logger
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseModel):
    """
    Database connection settings.
    """
    url: PostgresDsn
    max_connections: int = 20
    echo: bool = False

    @field_validator("url")
    @classmethod
    def validate_url(cls, v):
        if not v:
            raise ValueError("Database URL is not set.")
        return v


class Settings(BaseSettings):
    """
    App settings loaded from enviroment variables.
    """
    DATABASE: DatabaseSettings
    BOT_TOKEN: str
    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__"
    )

    def __init__(self, **data):
        super().__init__(**data)
        logger.info("⚙️ Settings loaded.")
        logger.debug(f"🐘 Database URL: {self.DATABASE.url}")
        logger.debug(f"🤖 Bot token: {self.BOT_TOKEN[:5]}***")
        logger.debug(f"🪵 Log level: {self.LOG_LEVEL}")

settings = Settings()
