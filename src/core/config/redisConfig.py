from pydantic import BaseModel, SecretStr

class RedisConfig(BaseModel):
    host : str = "localhost"
    port : str = "6379"
    password : SecretStr = "1111"
    db : str = "0"