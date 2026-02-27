import grpc
from kirt08_contracts.account import account_pb2, account_pb2_grpc

from src.core.db.models import UserResponse

from src.apps.account import Account

from src.apps.shared.exceptions import(
    ProblemsWithRedisException,
)

from src.apps.otp.exceptions import (
    IncorrectCodeException,
    CodeNotFoundException,
)

from src.apps.account.exceptions import (
    EmailAlreadyInUseException,
    PendingNotFoundException,
    IncorrectEmailException,
    PhoneAlreadyInUseException,
    IncorrectPhoneException,
)

class gRPC_Account_Server:
    def __init__(self, account : Account):
        self.service = account_pb2_grpc.AccountServiceServicer
        self.account = account

    async def GetAccount(self, request, context):
        """
        request.user_id : int64 -> User
        """
        try:
            res : UserResponse = await self.account.getAccount(request.id)
            response = account_pb2.GetAccountResponse(
                id=res.id,
                phone=res.phone,
                email=res.email,
                is_phone_verified=res.is_phone_verified,
                is_email_verified=res.is_email_verified,
                role=account_pb2.Role.Value(res.role.name),
            )
            return response
        except Exception as e:
            await context.abort(grpc.StatusCode.INTERNAL, "Something went wrong ...")

    async def InitEmailChange(self, request, context):
        """
        request.email : str
        request.id : int64
        """
        try:
            res = await self.account.initEmailChange(request.email, request.id)
            response = account_pb2.InitEmailChangeResponse(
                ok = True
            )
            return response
        except EmailAlreadyInUseException:
            await context.abort(EmailAlreadyInUseException.grpc_status, EmailAlreadyInUseException.message)
        except ProblemsWithRedisException:
            await context.abort(ProblemsWithRedisException.grpc_status, ProblemsWithRedisException.message)
        # except Exception as e:
        #     await context.abort(grpc.StatusCode.INTERNAL, "Something went wrong ...")

    async def ConfirmEmailChange(self, request, context):
        """
        request.email : str
        request.code : str
        request.id : int
        """
        try:
            res = await self.account.confirmEmailChange(request.email, request.code, request.id)
            response = account_pb2.InitEmailChangeResponse(
                ok = True
            )
            return response
        except PendingNotFoundException:
            await context.abort(PendingNotFoundException.grpc_status, PendingNotFoundException.message)
        except IncorrectEmailException:
            await context.abort(IncorrectEmailException.grpc_status, IncorrectEmailException.message)
        except IncorrectCodeException:
            await context.abort(IncorrectCodeException.grpc_status, IncorrectCodeException.message)
        except CodeNotFoundException:
            await context.abort(CodeNotFoundException.grpc_status, CodeNotFoundException.message)
        except Exception as e:
            await context.abort(grpc.StatusCode.INTERNAL, "Something went wrong ...")

    async def InitPhoneChange(self, request, context):
        """
        request.phone : str
        request.id : int64
        """
        try:
            res = await self.account.initPhoneChange(request.phone, request.id)
            response = account_pb2.InitPhoneChangeResponse(
                ok = True
            )
            return response
        except PhoneAlreadyInUseException:
            await context.abort(PhoneAlreadyInUseException.grpc_status, PhoneAlreadyInUseException.message)
        except ProblemsWithRedisException:
            await context.abort(ProblemsWithRedisException.grpc_status, ProblemsWithRedisException.message)
        except Exception as e:
            await context.abort(grpc.StatusCode.INTERNAL, "Something went wrong ...")

    async def ConfirmPhoneChange(self, request, context):
        """
        request.phone : str
        request.code : str
        request.id : int
        """
        try:
            res = await self.account.confirmPhoneChange(request.phone, request.code, request.id)
            response = account_pb2.InitPhoneChangeResponse(
                ok = True
            )
            return response
        except PendingNotFoundException:
            await context.abort(PendingNotFoundException.grpc_status, PendingNotFoundException.message)
        except IncorrectPhoneException:
            await context.abort(IncorrectPhoneException.grpc_status, IncorrectPhoneException.message)
        except IncorrectCodeException:
            await context.abort(IncorrectCodeException.grpc_status, IncorrectCodeException.message)
        except CodeNotFoundException:
            await context.abort(CodeNotFoundException.grpc_status, CodeNotFoundException.message)
        except Exception as e:
            await context.abort(grpc.StatusCode.INTERNAL, "Something went wrong ...")