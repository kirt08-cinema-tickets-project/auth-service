import logging

from src.core.config import settings
from src.core.redis_db import RedisService

from src.apps.otp.service import service_generate_code


log = logging.getLogger(__name__)
logging.basicConfig(
    format=settings.logger.format, 
    level=settings.logger.log_level,
)

class Otp:
    async def send_otp(identifier : str, type_ : str, redis : RedisService):
        code, hashed_code = service_generate_code()
        key = "otp:" + str(type_) + ":" + str(identifier)
        res = await redis.set(key, hashed_code, ex=500)
        log.info(f"code: {code} with redis res: {res}")
        return res
