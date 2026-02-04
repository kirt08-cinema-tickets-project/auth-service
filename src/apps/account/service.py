from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession 

from src.core.db.models import UsersORM, UserResponse

async def service_find_user_by_id(user_id : int, session : AsyncSession) -> UserResponse:
    user_orm = ( await session.execute(
        select(UsersORM)
        .filter_by(id = user_id)
    )).scalar_one()
    user_dto = UserResponse.model_validate(user_orm)
    return user_dto