from pydantic import BaseModel


class RmqConfig(BaseModel):
    user: str = ""
    password: str = ""
    host: str = ""
    port: str = ""

    @property
    def url(self) -> str:
        return f"amqp://{self.user}:{self.password}@{self.host}:{self.port}/"