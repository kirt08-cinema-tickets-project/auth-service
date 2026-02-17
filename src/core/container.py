from src.apps.otp import Otp
from src.apps.auth import Auth
from src.apps.account import Account
from src.apps.telegram import Telegram

from src.core.db import db
from src.core.redis_db import get_redis

from src.core.rabbitmq import (
    RabbitMQConnection,
    RabbitMQPublisher,
    Service_RMQ,
)
from src.core.config import settings


async def init_objects():
    rmq_publisher = RabbitMQPublisher(
        connection = RabbitMQConnection(
            url = settings.rmq.url
        )
    )
    await rmq_publisher.start()
    rmq_service = Service_RMQ(rmq_publisher)

    redis = await get_redis()
    otp = Otp(redis, rmq_service)

    auth = Auth(db, otp)
    account = Account(db, otp)
    telegram = Telegram(db, redis)
    return otp, auth, account, telegram