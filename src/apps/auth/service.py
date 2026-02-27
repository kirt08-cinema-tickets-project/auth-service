from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.utils import token
from src.core.config import settings

from src.core.db.models.users import UsersORM
from src.apps.auth.exceptions import (
    TokenException,
)

async def service_update_verified_field(identifier: str, type_: str, session : AsyncSession) -> tuple[int, bool]:
    """
    Update field 'is_phone_verified' or 'is_email_verified' depending on type_
    Return tuple [id, is_first_time]
    """
    is_first_time = False
    if type_ == "phone":
        user_orm = ( await session.execute(
            select(UsersORM)
            .filter_by(phone = identifier)
        )).scalar_one()
        if not user_orm.is_phone_verified:
            user_orm.is_phone_verified = True
            session.add(user_orm)
            await session.commit()
            is_first_time = True
    else:
        user_orm = ( await session.execute(
            select(UsersORM)
            .filter_by(email = identifier)
        )).scalar_one()
        if not user_orm.is_email_verified:
            user_orm.is_email_verified = True
            session.add(user_orm)
            await session.commit()
            is_first_time = True

    return (user_orm.id, is_first_time)

async def service_refresh(refresh_token : str) -> dict[str, str]:
    res : dict[bool, str] = token.verify_token(refresh_token)
    if not res.get("valid"):
        raise TokenException(res.get("reason"))
    new_tokens : dict[str, str] = {
        "access_token": token.generate_token(res.get("payload"), settings.passport.access_ttl),
        "refresh_token": token.generate_token(res.get("payload"), settings.passport.refresh_ttl),
    }
    return new_tokens