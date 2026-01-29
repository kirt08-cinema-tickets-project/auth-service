from pydantic import BaseModel, SecretStr
from sqlalchemy import URL


class DatabaseConfig(BaseModel):
    username : str = "test"
    password : SecretStr = "test"
    host : str = "test"
    port : str = "test"
    name : str = "test"

    echo : bool = True

    @property
    def async_url(self) -> URL:
        return URL.create(
            drivername="postgresql+asyncpg",
            username=self.username,
            password=self.password.get_secret_value(),
            host = self.host,
            port=self.port,
            database=self.name
        )