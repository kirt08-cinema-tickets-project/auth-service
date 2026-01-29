import logging
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import settings
from src.core.db import db

from src.apps.auth.schemas import UserRequest, UserResponse
from src.apps.auth.service import (
    service_create_user, 
    service_find_user_by_phone, 
    service_find_user_by_email
)
from src.apps.auth.exceptions import UserAlreadyExistsException

log = logging.getLogger(__name__)
logging.basicConfig(
    format=settings.logger.format, 
    level=settings.logger.log_level,
)

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/create", response_model = UserResponse)
async def create_user(
    data : UserRequest,
    session : AsyncSession = Depends(db.get_db),
) -> UserResponse:
    try:
        user = await service_create_user(data, session)
    except UserAlreadyExistsException:
        log.warning("Failed to create user. Such User Already Exist Exception")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Dublicate is not allowed. Such user already exists."
        )
    except:
        log.warning("Failed to crete user. Unknown Exception.")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong."
        )
    return user

@router.get("/check_user_by_phone")
async def check_user_by_phone(
    phone : Annotated[str, Query(...)],
    session : AsyncSession = Depends(db.get_db),
) -> dict[str, bool]:
    try:
        user = await service_find_user_by_phone(phone, session)
        if user:
            return {"exists": True}
        else:
            return {"exists": False}
    except:
        log.warning("Failed to check user by phone. Unknown Exception.")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong."
        )
    
@router.get("/check_user_by_email")
async def check_user_by_email(
    email : Annotated[str, Query(...)],
    session : AsyncSession = Depends(db.get_db),
) -> dict[str, bool]:
    try:
        user = await service_find_user_by_email(email, session)
        if user:
            return {"exists": True}
        else:
            return {"exists": False}
    except:
        log.warning("Failed to check user by email. Unknown Exception.")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong."
        )