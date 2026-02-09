import json
import random
import logging
import urllib.parse

from src.core.db import DataBase
from src.core.utils import token
from src.core.config import settings
from src.core.redis_db import RedisService

from src.core.db.models.schemas import (
    UserRequest,
    UserResponse,
    UserUpdate,
)

from src.apps.shared.exceptions import (
    ProblemsWithRedisException,
)

from src.apps.shared.service import (
    service_find_user_by_phone,
    service_create_user,
    service_user_update,
)

from src.apps.telegram.service import (
    service_find_user_by_telegramid,
    service_check_telegram_signature,
)

from src.apps.telegram.exceptions import (
    TelegramSignatureException,
    SessionNotFoundException,
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
                    "access_token": token.generate_token(str(exists.id), settings.passport.access_ttl),
                    "refresh_token": token.generate_token(str(exists.id), settings.passport.refresh_ttl)
                }
            
        res = True # not None object
        while res is not None:
            session_id = str(random.randbytes(16).hex())
            key = "telegram_session:" + session_id
            res = await self.redis.get(key)

        value = {
            "telegram_id": data.get("id"),
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
    
    async def telegramComplete(self, session_id: str, phone: str) -> str:
        key = "telegram_session:" + session_id
        raw = await self.redis.get(key)

        if raw is None:
            raise SessionNotFoundException
        
        raw = raw.decode("utf-8")
        data : dict[str, str] = json.loads(raw)

        async with self.db.session() as session:
            user = await service_find_user_by_phone(phone, session)

            if user is None:
                new_user = UserRequest(phone = phone)
                await service_create_user(new_user, session)
            
            user_for_update = UserUpdate(
                                    phone = phone,
                                    telegram_id=data.get("telegram_id"),
                                    is_phone_verified=True
                                )
            user = await service_user_update(user_for_update, session)
        
        tokens = {
            "access_token": token.generate_token(str(user.id), settings.passport.access_ttl),
            "refresh_token": token.generate_token(str(user.id), settings.passport.refresh_ttl)
        }
        
        tokens_key = "telegram_tokens:" + session_id
        await self.redis.set(
            tokens_key,
            json.dumps(tokens),
            120
        )
        await self.redis.delete(key)
        return session_id
    
    async def telegramConsume(self, session_id: str) -> dict[str, str]:
        tokens_key = "telegram_tokens:" + session_id
        raw = await self.redis.get(tokens_key)

        if raw is None:
            raise SessionNotFoundException
        
        raw = raw.decode("utf-8")
        tokens : dict[str, str] = json.loads(raw)

        await self.redis.delete(tokens_key)
        return tokens