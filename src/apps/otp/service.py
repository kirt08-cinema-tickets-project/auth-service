import logging
import random
import hashlib
import hmac

from src.core.redis_db import RedisService
from src.core.config import settings
from src.core.utils import token

from src.apps.otp.exceptions import (
    IncorrectCodeException,
    CodeNotFoundException,
)

log = logging.getLogger(__name__)
logging.basicConfig(
    format=settings.logger.format, 
    level=settings.logger.log_level,
)

def service_generate_code() -> tuple[str, str]:
    code : str = str(random.randint(100000, 999999))
    hashed_code : str = hashlib.sha256(code.encode()).hexdigest()
    return (code, hashed_code)

async def service_verify_otp(identifier : str, type_ : str, code : str, payload : str, redis : RedisService) -> dict[str, str]:
    key = "otp:" + str(type_) + ":" + str(identifier)
    hashed_real_code: bytes = await redis.get(key)

    if hashed_real_code is None:
        raise CodeNotFoundException
    
    hashed_real_code = hashed_real_code.decode()
    hashed_user_code = hashlib.sha256(code.encode()).hexdigest()

    res = hmac.compare_digest(hashed_real_code, hashed_user_code)
    if not res:
        raise IncorrectCodeException

    access_token = await service_generate_access_token(payload)
    refresh_token = await service_generate_refresh_token(payload)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
    }

async def service_generate_access_token(payload: str):
    return token.generate_token(str(payload), settings.passport.access_ttl)

async def service_generate_refresh_token(payload: str):
    return token.generate_token(str(payload), settings.passport.refresh_ttl)
