import os
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


from src.core.config.rmqConfig import RmqConfig
from src.core.config.grpcConfig import GrpcConfig
from src.core.config.redisConfig import RedisConfig
from src.core.config.dbConfig import DatabaseConfig
from src.core.config.loggerConfig import LoggerConfig
from src.core.config.passportConfig import PassportConfig
from src.core.config.telegramConfig import TelegramConfig
from src.core.config.rmqQueueConfig import RmqQueueConfig


BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
env_name = os.getenv("ENVIRONMENT", "development").lower()
env_file = BASE_DIR / f".env.{env_name}.local"

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file= env_file,
        env_prefix="AUTH_SERVICE__",
        env_nested_delimiter="__"
    )
    db : DatabaseConfig = DatabaseConfig()
    logger : LoggerConfig = LoggerConfig()
    redis_db : RedisConfig = RedisConfig()
    passport : PassportConfig = PassportConfig()
    telegram : TelegramConfig = TelegramConfig()
    rmq : RmqConfig = RmqConfig()
    rmq_queue : RmqQueueConfig = RmqQueueConfig()
    grpc: GrpcConfig = GrpcConfig()

settings = Settings()
