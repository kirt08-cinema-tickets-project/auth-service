from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.auth.models import UsersORM
from src.apps.auth.schemas import UserResponse, UserRequest
from src.apps.auth.exceptions import UserAlreadyExistsException

from src.apps.otp.router import Otp

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

async def service_update_verified_field(identifier: str, type_: str, session : AsyncSession) -> None:
    """
    Update field 'is_phone_verified' or 'is_email_verified' depending on type_
    """
    if type_ == "phone":
        user_orm = ( await session.execute(
            select(UsersORM)
            .filter_by(phone = identifier)
        )).scalar_one()
        user_orm.is_phone_verified = True
        session.add(user_orm)
        await session.commit()
    else:
        user_orm = ( await session.execute(
            select(UsersORM)
            .filter_by(email = identifier)
        )).scalar_one()
        user_orm.is_email_verified = True
        session.add(user_orm)
        await session.commit()

    