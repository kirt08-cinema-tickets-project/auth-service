import logging

from src.core.redis_db import RedisService

from src.apps.shared.exceptions import ProblemsWithRedisException

from src.apps.otp.service import (
    service_generate_code,
    service_verify_otp,
)

from src.apps.otp.exceptions import (
    IncorrectCodeException,
    CodeNotFoundException,
)


log = logging.getLogger(__name__)

class Otp:
    def __init__(self, redis : RedisService):
        self.redis = redis

    async def send_otp(self, identifier : str, type_ : str) -> list[str]:
        code, hashed_code = service_generate_code()
        key = "otp:" + str(type_) + ":" + str(identifier)
        try:
            res = await self.redis.set(key, hashed_code, ex=500)
        
            if not res:
                log.error(f"send_otp: error with redis, res: {res}")
                raise ProblemsWithRedisException
            
            log.info(f"code: {code} with redis res: {res}")
            return [code, hashed_code]
        except:
            raise ProblemsWithRedisException
        
    
    async def verify_otp(
        self,
        identifier : str,
        type_ : str,
        code : str,
        user_id : str
    ) -> dict[str, str]:
        try:
            res = await service_verify_otp(identifier, type_, code, user_id, self.redis)
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