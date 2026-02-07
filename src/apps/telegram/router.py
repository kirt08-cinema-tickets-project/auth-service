import json
import random
import logging
import urllib.parse

from src.core.db import DataBase
from src.core.utils import token
from src.core.config import settings
from src.core.redis_db import RedisService

from src.apps.shared.exceptions import (
    ProblemsWithRedisException,
)

from src.apps.telegram.service import (
    service_find_user_by_telegramid,
    service_check_telegram_signature,
)

from src.apps.telegram.exceptions import (
    TelegramSignatureException,
)



log = logging.getLogger(__name__)

class Telegram:
    def __init__(self, db : DataBase, redis : RedisService):
        self.db = db
        self.redis = redis

    async def telegramInit(self) -> str:
        url = "https://oauth.telegram.org/auth"
        query_params = {
            "bot_id": settings.telegram.bot.id,
            "origin": settings.telegram.redirect_origin,
            "request_access": "write",
            "return_to": settings.telegram.redirect_origin
        }
        encoded_params = urllib.parse.urlencode(query_params)
        final_url = f"{url}?{encoded_params}"
        return final_url
    
    async def telegramVerify(self, data : dict[str, str]) -> str | dict[str, str]:
        isValid = service_check_telegram_signature(data)
        if not isValid:
            raise TelegramSignatureException

        async with self.db.session() as session:
            exists = await service_find_user_by_telegramid(data.get("id"), session)
            if exists is not None and exists.phone is not None:
                return {
                    "access_token": token.generate_token(exists.id, settings.passport.access_ttl),
                    "refresh_token": token.generate_token(exists.id, settings.passport.refresh_ttl)
                }
            
        res = True # not None object
        while res is not None:
            session_id = str(random.randbytes(16).hex())
            key = "telegram_session:" + session_id
            res = await self.redis.get(key)

        value = {
            "telegramID": data.get("id"),
            "username": data.get("username")
        }
        try:
            await self.redis.set(
                key,
                json.dumps(value),
                ex=300
            )
        except:
            raise ProblemsWithRedisException
        
        url = f"https://t.me/{settings.telegram.bot.username}?start={session_id}"
        return url