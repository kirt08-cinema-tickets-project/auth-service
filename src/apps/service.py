from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.models import UsersORM
from src.apps.schemas import UserResponse, UserRequest
from src.apps.exceptions import UserAlreadyExistsException

async def service_find_user_by_phone(
    phone : str,
    session : AsyncSession,
) -> UserResponse | None:
    user_orm = ( await session.execute(
        select(UsersORM)
        .filter_by(phone = phone)
    )).scalar_one_or_none()
    if user_orm is not None:
        user_dto = UserResponse.model_validate(user_orm)
    return user_dto if user_orm is not None else None

async def service_find_user_by_email(
    email : str,
    session : AsyncSession,
) -> UserResponse | None:
    user_orm = ( await session.execute(
        select(UsersORM)
        .filter_by(email = email)
    )).scalar_one_or_none()
    if user_orm is not None:
        user_dto = UserResponse.model_validate(user_orm)
    return user_dto if user_orm is not None else None

async def service_create_user(
    data : UserRequest,
    session : AsyncSession,
) -> UserResponse:
    if data.phone is not None:
        user = await service_find_user_by_phone(data.phone, session)
        if user:
            raise UserAlreadyExistsException
    else:
        user = await service_find_user_by_email(data.email, session)
        if user:
            raise UserAlreadyExistsException
    user = UsersORM(
        phone = data.phone,
        email = data.email,
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user

    