from pydantic import BaseModel, SecretStr
from sqlalchemy import URL


class DatabaseConfig(BaseModel):
    username : str = "posgres"
    password : SecretStr = "1111"
    host : str = "localhost"
    port : str = "5432"
    name : str = "postgres"

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