from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db.models.users import UsersORM
from src.core.db.models.schemas import (
    UserRequest,
    UserResponse,
    UserUpdate,
)

from src.apps.shared.exceptions import (
    UserAlreadyExistsException,
    NotEnoughtDataForUpdateException,
    UserNotFoundException,
)


async def service_find_user_by_id(user_id : int, session : AsyncSession) -> UserResponse:
    user_orm = ( await session.execute(
        select(UsersORM)
        .filter_by(id = user_id)
    )).scalar_one()
    user_dto = UserResponse.model_validate(user_orm)
    return user_dto

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

async def service_update_user_email(
    user_id : int,
    email : str,
    session : AsyncSession
) -> None:
    res = ( await session.execute(select(UsersORM)
                                .filter_by(id = user_id)) ).scalar_one()
    res.email = email
    res.is_email_verified = True
    session.add(res)
    await session.commit()

async def service_update_user_phone(
    user_id : int,
    phone : str,
    session : AsyncSession
) -> None:
    res = ( await session.execute(select(UsersORM)
                                .filter_by(id = user_id)) ).scalar_one()
    res.phone = phone
    res.is_phone_verified = True
    session.add(res)
    await session.commit()

async def service_user_update(
    data : UserUpdate,
    session : AsyncSession
) -> UserResponse:
    if data.phone is not None:
        user_dto : UserResponse = await service_find_user_by_phone(data.phone, session)
    elif data.email is not None:
        user_dto : UserResponse = await service_find_user_by_email(data.email, session)
    else:
        raise NotEnoughtDataForUpdateException
    
    if user_dto is None:
        raise UserNotFoundException
    
    user_from_db = await session.execute(select(UsersORM).filter_by(id = user_dto.id))
    user_orm: UsersORM = user_from_db.scalar_one()

    update_fields = data.model_dump(exclude_unset=True)
    for field, value in update_fields.items(): 
        setattr(user_orm, field, value)

    await session.commit()
    await session.refresh(user_orm)

    return UserResponse.model_validate(user_orm)