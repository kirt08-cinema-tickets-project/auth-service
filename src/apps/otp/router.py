import logging

from src.core.config import settings
from src.core.redis_db import RedisService

from src.apps.otp.service import (
    service_generate_code,
    service_verify_otp,
)

from src.apps.otp.exceptions import (
    ProblemsWithRedisException,
    IncorrectCodeException,
    CodeNotFoundException,
)

log = logging.getLogger(__name__)
logging.basicConfig(
    format=settings.logger.format, 
    level=settings.logger.log_level,
)

class Otp:
    async def send_otp(identifier : str, type_ : str, redis : RedisService) -> list[str]:
        code, hashed_code = service_generate_code()
        key = "otp:" + str(type_) + ":" + str(identifier)
        try:
            res = await redis.set(key, hashed_code, ex=500)
        
            if not res:
                log.error(f"send_otp: error with redis, res: {res}")
                raise ProblemsWithRedisException
            
            log.info(f"code: {code} with redis res: {res}")
            return [code, hashed_code]
        except:
            raise ProblemsWithRedisException
        
    
    async def verify_otp(
        identifier : str,
        type_ : str,
        code : str,
        user_id : str,
        redis : RedisService,
    ) -> dict[str, str]:
        try:
            res = await service_verify_otp(identifier, type_, code, user_id, redis)
            return res
        except IncorrectCodeException:
            log.error("incorrect code")
            raise
        except CodeNotFoundException:
            log.error("code not found in redis")
            raise
        except Exception as e:
            log.error(f"error: {e}")
            raise