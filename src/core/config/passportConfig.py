from pydantic import BaseModel


class PassportConfig(BaseModel):
    secret_key: str = "test"
    access_ttl: int = 1
    refresh_ttl: int = 1
    hmac_domain: str = "test"