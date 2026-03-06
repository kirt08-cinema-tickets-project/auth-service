import logging

from src.core.db import DataBase

from src.core.grpc_client import UsersClient

from src.core.db.models.schemas import (
    UserRequest,
)

from src.apps.shared.service import (
    service_create_user,
)

from src.apps.otp import Otp

from src.apps.auth.service import (
    service_update_verified_field,
    service_refresh,
)

log = logging.getLogger(__name__)

class Auth:
    def __init__(self, db : DataBase, otp : Otp, user_client: UsersClient):
        self.db = db
        self.otp = otp
        self.user_client = user_client


    async def sendOtp(self, identifier: str, type_: str) -> bool:
        async with self.db.session() as session:
            data = UserRequest()
            if type_ == "phone":
                data.phone = identifier
            else:
                data.email = identifier
            try:
                res = await service_create_user(data, session)
            except Exception as e:
                log.info(e)

        res = await self.otp.send_otp(identifier, type_)
        return True


    async def verifyOtp(self, identifier : str, type_ : str, code : str) -> dict[str, str]:
        async with self.db.session() as session:
            user_id, is_first_time = await service_update_verified_field(identifier, type_, session)

        res = await self.otp.verify_otp(identifier, type_, code, user_id)
        if is_first_time:
            await self.user_client.create_user(str(user_id))

        return res
        

    async def refresh(self, refresh_token : str) -> dict[str, str]:
        res = await service_refresh(refresh_token)
        return res