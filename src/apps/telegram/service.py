import hashlib
import hmac

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import settings
from src.core.db.models import UsersORM, UserResponse

async def service_find_user_by_telegramid(telegram_id : str, session : AsyncSession) -> UserResponse | None:
    user_orm = ( await session.execute(select(UsersORM)
                                       .filter_by(telegram_id = telegram_id)
                                       )).scalar_one_or_none()
    return UserResponse.model_validate(user_orm) if user_orm is not None else None

def service_check_telegram_signature(data : dict[str, str]) -> bool:
    received_hash = data.get("hash")
    if received_hash is None:
        return False
    
    sorted_data = sorted(data.items())
    data_check_string = "\n".join(f"{k}={v}" for k, v in sorted_data if k != "hash")
    bot_token_str = (f"{settings.telegram.bot.id}:{settings.telegram.bot.token}").encode()
    secret_key = hashlib.sha256(bot_token_str).digest()
    calculate_hmac = hmac.new(
        secret_key,
        data_check_string.encode(),
        hashlib.sha256
    ).hexdigest()
    return received_hash == calculate_hmac