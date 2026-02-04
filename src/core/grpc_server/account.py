import grpc
from kirt08_contracts.account import account_pb2, account_pb2_grpc

from src.core.db.models import UserResponse

from src.apps.account import Account


class gRPC_Account_Server:
    def __init__(self):
        self.service = account_pb2_grpc.AccountServiceServicer

    async def GetAccount(self, request, context):
        """
        request.user_id : int64 -> User
        """
        try:
            res : UserResponse = await Account.getAccount(request.id)
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