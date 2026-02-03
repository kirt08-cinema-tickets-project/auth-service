from kirt08_tokens import Token

from src.core.config import settings


token = Token(
    hmac_domain=settings.passport.hmac_domain,
    secret_key=settings.passport.secret_key.get_secret_value(),
)