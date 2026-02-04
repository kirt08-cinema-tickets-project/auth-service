import logging

from src.core.db import db
from src.core.config import settings
from src.core.db.models import UserResponse

from src.apps.account.service import (
    service_find_user_by_id,
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