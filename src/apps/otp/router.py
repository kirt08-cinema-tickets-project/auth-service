import logging
from typing import Annotated

from fastapi import APIRouter, Depends, Query

from src.core.config import settings
from src.core.redis_db import RedisService, get_redis

from src.apps.otp.schemas import OtpRequest
from src.apps.otp.service import service_generate_code


log = logging.getLogger(__name__)
logging.basicConfig(
    format=settings.logger.format, 
    level=settings.logger.log_level,
)

router = APIRouter(prefix="/otp", tags=["auth"])

@router.get("/send")
async def send_otp(
    data : Annotated[OtpRequest, Query()],
    redis : RedisService = Depends(get_redis)
):
    code, hashed_code = service_generate_code()
    key = "otp:" + str(data.type) + ":" + str(data.identifier)
    res = await redis.set(key, hashed_code, ex=500)
    return code