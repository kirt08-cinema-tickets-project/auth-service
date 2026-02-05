import logging
import datetime

from src.core.redis_db.database import get_redis

from src.core.db import db
from src.core.config import settings
from src.core.db.models import UserResponse, PendingContactChangesRequest
from src.core.db.models.utils import Type

from src.core.db.service import (
    service_find_user_by_id,
    service_find_user_by_email,
    service_update_user_email,
    service_find_user_by_phone,
    service_update_user_phone,
)

from src.apps.otp import Otp

from src.apps.account.exceptions import (
    EmailAlreadyInUseException,
    PendingNotFoundException,
    IncorrectEmailException,
    PhoneAlreadyInUseException,
    PendingNotFoundException,
    IncorrectPhoneException,
)

from src.apps.account.service import (
    service_upsert_PendingChange,
    service_find_PendingChange,
    service_delete_PendingChange,
)


log = logging.getLogger(__name__)
logging.basicConfig(
    format=settings.logger.format, 
    level=settings.logger.log_level,
)

class Account:
    async def getAccount(user_id : int) -> UserResponse:
        async with db.session() as session:
            user : UserResponse = await service_find_user_by_id(user_id, session)
        return user
    
    async def initEmailChange(email : str, account_id : int) -> bool:
        async with db.session() as session:
            user : UserResponse = await service_find_user_by_email(email, session)
            if user:
                raise EmailAlreadyInUseException

            redis = await get_redis()
            code, hashed_code = await Otp.send_otp(email, "email", redis)
            
            now = int(datetime.datetime.now(datetime.timezone.utc).timestamp() * 1000)

            data = PendingContactChangesRequest(
                type = Type.email,
                value = email,
                codeHash = hashed_code,
                expiresAt = now + 5 * 60 * 1000,
            )
            res = await service_upsert_PendingChange(account_id, data, session)

            return True
        
    async def confirmEmailChange(email : str, code : str, account_id : int) -> bool:
        async with db.session() as session:
            try:
                pending = await service_find_PendingChange(account_id, Type.email, session)
            except:
                raise PendingNotFoundException
            
            if pending.value != email:
                raise IncorrectEmailException
            
            redis = await get_redis()
            await Otp.verify_otp(email, Type.email.value, code, account_id, redis)
            await service_update_user_email(account_id, email, session)
            await service_delete_PendingChange(account_id, Type.email, session)
            return True
        
    async def initPhoneChange(phone : str, account_id : int) -> bool:
        async with db.session() as session:
            user : UserResponse = await service_find_user_by_phone(phone, session)
            if user:
                raise PhoneAlreadyInUseException

            redis = await get_redis()
            code, hashed_code = await Otp.send_otp(phone, "phone", redis)
            
            now = int(datetime.datetime.now(datetime.timezone.utc).timestamp() * 1000)

            data = PendingContactChangesRequest(
                type = Type.phone,
                value = phone,
                codeHash = hashed_code,
                expiresAt = now + 5 * 60 * 1000,
            )
            res = await service_upsert_PendingChange(account_id, data, session)

            return True
        
    async def confirmPhoneChange(phone : str, code : str, account_id : int) -> bool:
        async with db.session() as session:
            try:
                pending = await service_find_PendingChange(account_id, Type.phone, session)
            except:
                raise PendingNotFoundException
            
            if pending.value != phone:
                raise IncorrectPhoneException
            
            redis = await get_redis()
            await Otp.verify_otp(phone, Type.phone.value, code, account_id, redis)
            await service_update_user_phone(account_id, phone, session)
            await service_delete_PendingChange(account_id, Type.phone, session)
            return True