import grpc
from kirt08_contracts.auth import auth_pb2, auth_pb2_grpc

from src.apps.shared.exceptions import (
    UserAlreadyExistsException,
    ProblemsWithRedisException,
    NotEnoughtDataForUpdateException,
    UserNotFoundException,
)

from src.apps.auth import Auth
from src.apps.auth.exceptions import (
    TokenException,
)

from src.apps.telegram import Telegram

from src.apps.telegram.exceptions import (
    TelegramSignatureException,
    SessionNotFoundException,
)

from src.apps.otp.exceptions import (
    IncorrectCodeException,
    CodeNotFoundException,
)

from src.core.rabbitmq.exceptions import (
    ProblemsWithRMQException,
)


class gRPC_Auth_Server:
    def __init__(self, auth : Auth, telegram : Telegram):
        self.service = auth_pb2_grpc.AuthServiceServicer
        self.auth = auth
        self.telegram = telegram

    async def SendOtp(self, request, context):
        """
        request.identifier 
        request.type       ["phone" | "email"]
        """
        try:
            response = auth_pb2.SendOtpResponse()
            res = await self.auth.sendOtp(request.identifier, request.type)
            response.ok = True
            return response
        except ProblemsWithRedisException:
            await context.abort(ProblemsWithRedisException.grpc_status, ProblemsWithRedisException.message)
        except UserAlreadyExistsException:
            await context.abort(UserAlreadyExistsException.grpc_status, UserAlreadyExistsException.message)
        except ProblemsWithRMQException:
            await context.abort(ProblemsWithRMQException.grpc_status, ProblemsWithRMQException.message)
        # except Exception as e:
        #     await context.abort(grpc.StatusCode.INTERNAL, "Something went wrong...")
        
    
    async def VerifyOtp(self, request, context):
        """
        request.identifier
        request.type       ["phone" | "email"]
        request.code
        """
        try:
            response = auth_pb2.VerifyOtpResponse()
            res : dict[str, str] = await self.auth.verifyOtp(request.identifier, request.type, request.code)
        except IncorrectCodeException:
            await context.abort(IncorrectCodeException.grpc_status, IncorrectCodeException.message)
        except CodeNotFoundException:
            await context.abort(CodeNotFoundException.grpc_status, CodeNotFoundException.message)
        # except Exception:
        #     await context.abort(grpc.StatusCode.INTERNAL, "Something went wrong...")

        response.access_token = res["access_token"]
        response.refresh_token = res["refresh_token"]
        return response
    

    async def Refresh(self, request, context):
        """
        request.refresh_token -> {access_token, refresh_token}
        """
        try:
            response = auth_pb2.RefreshResponse()
            res : dict[str, str] = await self.auth.refresh(request.refresh_token)
            response.access_token = res["access_token"]
            response.refresh_token = res["refresh_token"]
            return response
        except TokenException as e:
            await context.abort(e.grpc_status, e.message)
        # except Exception:
        #     await context.abort(grpc.StatusCode.INTERNAL, "Something went wrong...")


    async def TelegramInit(self, request, context):
        """
        request.Empty -> url
        """
        try:
            response = auth_pb2.TelegramInitResponse()
            res : str = await self.telegram.telegramInit()
            response.url = res
            return response
        except Exception:
            await context.abort(grpc.StatusCode.INTERNAL, "Something went wrong...")
    

    async def TelegramVerify(self, request, context):
        """
        request.query = map<string, string>
        """
        try:
            response = auth_pb2.TelegramVerifyResponse()
            query_dict = dict(request.query)
            res : dict[str, str] | str = await self.telegram.telegramVerify(query_dict)

            if isinstance(res, str):
                response.url = res
            else:
                response.tokens.access_token = res.get("access_token")
                response.tokens.refresh_token = res.get("refresh_token")
            return response
        except TelegramSignatureException:
            await context.abort(TelegramSignatureException.grpc_status, TelegramSignatureException.message)
        except Exception:
            await context.abort(grpc.StatusCode.INTERNAL, "Something went wrong...")


    async def TelegramComplete(self, request, context):
        """
        request.session_id
        request.phone
        """
        try:
            response = auth_pb2.TelegramCompleteResponse()
            res : str = await self.telegram.telegramComplete(request.session_id, request.phone)
            response.session_id = res
            return response
        except SessionNotFoundException:
           await context.abort(SessionNotFoundException.grpc_status, SessionNotFoundException.message)
        except UserAlreadyExistsException:
            await context.abort(UserAlreadyExistsException.grpc_status, UserAlreadyExistsException.message)
        except NotEnoughtDataForUpdateException:
            await context.abort(NotEnoughtDataForUpdateException.grpc_status, NotEnoughtDataForUpdateException.message)
        except UserNotFoundException:
            await context.abort(UserNotFoundException.grpc_status, UserNotFoundException.message)
        except Exception:
            await context.abort(grpc.StatusCode.INTERNAL, "Something went wrong...")


    async def TelegramConsume(self, request, context):
        try:
            response = auth_pb2.TelegramConsumeResponse()
            res : dict[str, str] = await self.telegram.telegramConsume(request.session_id)
            response.access_token = res.get("access_token")
            response.refresh_token = res.get("refresh_token")
            return response
        except SessionNotFoundException:
            await context.abort(SessionNotFoundException.grpc_status, SessionNotFoundException.message)
        except Exception:
            await context.abort(grpc.StatusCode.INTERNAL, "Something went wrong...")
