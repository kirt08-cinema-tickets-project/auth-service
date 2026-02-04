from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.utils import token
from src.core.config import settings

from src.core.db.models.users import UsersORM
from src.core.db.models.schemas import UserResponse, UserRequest
from src.apps.auth.exceptions import (
    UserAlreadyExistsException,
    TokenException,
)

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
        return user_orm.id
    else:
        user_orm = ( await session.execute(
            select(UsersORM)
            .filter_by(email = identifier)
        )).scalar_one()
        user_orm.is_email_verified = True
        session.add(user_orm)
        await session.commit()
        return user_orm.id

async def service_refresh(refresh_token : str) -> dict[str, str]:
    res : dict[bool, str] = token.verify_token(refresh_token)
    if not res.get("valid"):
        raise TokenException(res.get("reason"))
    new_tokens : dict[str, str] = {
        "access_token": token.generate_token(res.get("payload"), settings.passport.access_ttl),
        "refresh_token": token.generate_token(res.get("payload"), settings.passport.refresh_ttl),
    }
    return new_tokens