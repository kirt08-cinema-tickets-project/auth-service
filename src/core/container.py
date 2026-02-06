from src.apps.otp import Otp
from src.apps.auth import Auth
from src.apps.account import Account
from src.apps.telegram import Telegram

from src.core.db import db
from src.core.redis_db import get_redis

async def init_objects():
    redis = await get_redis()
    otp = Otp(redis)

    auth = Auth(db, otp)
    account = Account(db, otp)
    telegram = Telegram(db, redis)
    return otp, auth, account, telegram