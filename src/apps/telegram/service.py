from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db.models import UsersORM, UserResponse

async def service_find_user_by_telegramid(telegram_id : str, session : AsyncSession) -> UserResponse | None:
    user_orm = ( await session.execute(select(UsersORM)
                                       .filter_by(telegram_id = telegram_id)
                                       )).scalar_one_or_none()
    return UserResponse.model_validate(user_orm) if user_orm is not None else None