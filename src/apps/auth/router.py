import logging

from src.core.db import db
from src.core.db.service import service_create_user

from src.core.config import settings
from src.core.redis_db import get_redis

from src.apps.otp import Otp

from src.apps.auth.service import (
    service_update_verified_field,
    service_refresh,
)

from src.core.db.models.schemas import (
    UserRequest,
)

log = logging.getLogger(__name__)
logging.basicConfig(
    format=settings.logger.format, 
    level=settings.logger.log_level,
)

class Auth:
    async def sendOtp(identifier: str, type_: str) -> bool:
        async with db.session() as session:
            data = UserRequest()
            if type_ == "phone":
                data.phone = identifier
            else:
                data.email = identifier
            res = await service_create_user(data, session)

        redis = await get_redis()
        res = await Otp.send_otp(identifier, type_, redis)

        return True


    async def verifyOtp(identifier : str, type_ : str, code : str) -> dict[str, str]:
        async with db.session() as session:
            user_id = await service_update_verified_field(identifier, type_, session)
        
        redis = await get_redis()
        res = await Otp.verify_otp(identifier, type_, code, user_id, redis)

        return res
        
    async def refresh(refresh_token : str) -> dict[str, str]:
        res = await service_refresh(refresh_token)
        return res