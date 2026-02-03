from pydantic import BaseModel, SecretStr


class PassportConfig(BaseModel):
    secret_key: SecretStr = "test"
    access_ttl: int = 1
    refresh_ttl: int = 1
    hmac_domain: str = "test"