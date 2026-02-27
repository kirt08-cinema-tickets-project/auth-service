import logging
import datetime

from src.core.db import DataBase
from src.core.config import settings
from src.core.db.models import UserResponse, PendingContactChangesRequest
from src.core.db.models.utils import Type

from src.core.rabbitmq import Service_RMQ

from src.apps.shared.service import (
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


class Account:
    def __init__(self, db : DataBase, otp : Otp):
        self.db = db
        self.otp = otp

    async def getAccount(self, user_id : int) -> UserResponse:
        async with self.db.session() as session:
            user : UserResponse = await service_find_user_by_id(user_id, session)
        return user
    
    async def initEmailChange(self, email : str, account_id : int) -> bool:
        async with self.db.session() as session:
            user : UserResponse = await service_find_user_by_email(email, session)
            if user:
                raise EmailAlreadyInUseException

            code, hashed_code = await self.otp.send_email_change_otp(email)

            now = int(datetime.datetime.now(datetime.timezone.utc).timestamp() * 1000)

            data = PendingContactChangesRequest(
                type = Type.email,
                value = email,
                codeHash = hashed_code,
                expiresAt = now + 5 * 60 * 1000,
            )
            res = await service_upsert_PendingChange(account_id, data, session)

            return True
        
    async def confirmEmailChange(self, email : str, code : str, account_id : int) -> bool:
        async with self.db.session() as session:
            try:
                pending = await service_find_PendingChange(account_id, Type.email, session)
            except:
                raise PendingNotFoundException
            
            if pending.value != email:
                raise IncorrectEmailException
            
            await self.otp.verify_otp(email, Type.email.value, code, account_id)
            await service_update_user_email(account_id, email, session)
            await service_delete_PendingChange(account_id, Type.email, session)
            return True