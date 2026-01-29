from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


from src.core.config.dbConfig import DatabaseConfig
from src.core.config.loggerConfig import LoggerConfig
from src.core.config.redisConfig import RedisConfig

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file= BASE_DIR / ".env",
        env_prefix="AUTH_SERVICE__",
        env_nested_delimiter="__"
    )
    db : DatabaseConfig = DatabaseConfig()
    logger : LoggerConfig = LoggerConfig()
    redis_db : RedisConfig = RedisConfig()

settings = Settings()
